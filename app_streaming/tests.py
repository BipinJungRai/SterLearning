import asyncio

from app_streaming.consumers import get_section
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.test import TestCase
from django.urls import path, re_path
from app_streaming.consumers import QuizConsumer
from app_quiz.models import Quiz, MultipleChoice, MultipleChoiceOptions, FillInBlank, FillInBlankSentence, Information, \
Attempt
import json

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User


class GetSectionTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(name='Test Quiz')

        self.mcq = MultipleChoice.objects.create(quiz=self.quiz, title='MCQ Question', position=1, points=10)
        MultipleChoiceOptions.objects.create(question=self.mcq, text='Option 1', correct=True)
        MultipleChoiceOptions.objects.create(question=self.mcq, text='Option 2', correct=False)

        self.fib = FillInBlank.objects.create(quiz=self.quiz, title='FIB Question', position=2)
        FillInBlankSentence.objects.create(question=self.fib, before='Before', blank='Blank', after='After', points=5)

        self.inf = Information.objects.create(quiz=self.quiz, title='Information', content='Content', position=3)

    def test_get_section_mcq(self):
        section = get_section(self.quiz, 1)
        self.assertEqual(section['section_type'], 'mcq')
        self.assertEqual(section['section']['title'], self.mcq.title)
        self.assertEqual(len(section['section']['options']), 2)

    def test_get_section_fib(self):
        section = get_section(self.quiz, 2)
        self.assertEqual(section['section_type'], 'fib')
        self.assertEqual(section['section']['title'], self.fib.title)
        self.assertEqual(len(section['section']['sentences']), 1)

    def test_get_section_inf(self):
        section = get_section(self.quiz, 3)
        self.assertEqual(section['section_type'], 'inf')
        self.assertEqual(section['section']['title'], self.inf.title)

    def test_get_section_end(self):
        section = get_section(self.quiz, 4)
        self.assertEqual(section['section_type'], 'end')


from asgiref.sync import sync_to_async
from django.contrib.auth.models import User


class QuizConsumerTests(TestCase):
    async def asyncSetUp(self):
        # Create your test data here
        self.user = await sync_to_async(User.objects.create_user)('testuser', 'test@example.com', 'testpassword')
        self.quiz = await sync_to_async(Quiz.objects.create)(name="Test Quiz")
        self.question = await sync_to_async(MultipleChoice.objects.create)(question_text="Test Question",
                                                                           quiz=self.quiz)
        self.option = await sync_to_async(MultipleChoiceOptions.objects.create)(option_text="Test Option",
                                                                                question=self.question, correct=True)
        self.attempt = await sync_to_async(Attempt.objects.create)(user=self.user, quiz=self.quiz, completed=False,
                                                                   quiz_open=True)

        self.application = URLRouter([
            re_path(r"^ws/quiz/$", QuizConsumer.as_asgi()),
        ])

    def setUp(self):
        asyncio.run(self.asyncSetUp())

    async def test_connect(self):
        communicator = WebsocketCommunicator(self.application, "/ws/quiz/", user=self.user)
        connected, _ = await communicator.connect()
        assert connected is True
        response = await communicator.receive_from()
        data = json.loads(response)
        self.assertEqual(data["type"], "connected")
        await communicator.disconnect()

    async def test_receive_answer_mcq(self):
        communicator = WebsocketCommunicator(self.application, "/ws/quiz/", user=self.user)
        await communicator.connect()
        await communicator.send_to(json.dumps({
            "type": "answer",
            "section_type": "mcq",
            "question_id": self.question.id,
            "selected_id": self.option.id
        }))
        response = await communicator.receive_from()
        data = json.loads(response)
        self.assertEqual(data["type"], "validated_mcq_answer")
        self.assertEqual(data["correct"], True)
        self.assertEqual(data["awarded"], self.question.points)
        await communicator.disconnect()
