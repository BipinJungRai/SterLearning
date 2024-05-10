import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from app_streaming.consumers import get_section
from app_quiz.models import Quiz, MultipleChoice, MultipleChoiceOptions, FillInBlank, FillInBlankSentence, Information, \
    Attempt
from django.test import TestCase, AsyncClient
from channels.testing import WebsocketCommunicator
from app_streaming.consumers import QuizConsumer


class GetSectionTest(TestCase):
    """
    Test the get_section function in the consumers.py file.
    """
    def setUp(self):
        """
        A method that is run before each test.
        """
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


class QuizConsumerTest(TestCase):
    @database_sync_to_async
    def create_user(self):
        return get_user_model().objects.create_user(username='testuser', password='testpassword')

    @database_sync_to_async
    def create_quiz(self):
        # Replace with your actual Quiz creation code...
        return Quiz.objects.create(name='Test Quiz')

    async def connect(self):
        # Create a user
        self.user = await self.create_user()

        # Create a quiz
        self.quiz = await self.create_quiz()

        # Create an AsyncClient instance
        self.client = AsyncClient()

        # Log in the user
        await sync_to_async(self.client.login)(username='testuser', password='testpassword')

        # Create a communicator for the QuizConsumer
        self.communicator = WebsocketCommunicator(QuizConsumer.as_asgi(), "/ws/quiz/")

        # Set the user in the communicator's scope
        self.communicator.scope['user'] = self.user

        # Connect to the websocket
        connected, _ = await self.communicator.connect()
        assert connected

        # Receive and discard the first message from the consumer
        _ = await self.communicator.receive_from()

    async def test_disconnect(self):
        await self.connect()

        # Send a message to the websocket
        await self.communicator.send_to(json.dumps({"type": "start", "qid": self.quiz.id}))

        # Receive and discard the first message from the consumer
        _ = await self.communicator.receive_from()

        # Disconnect from the websocket
        await self.communicator.disconnect()

        # Check if the quiz_open attribute of the attempt is False
        attempt = await sync_to_async(Attempt.objects.get)(user=self.user)
        self.assertFalse(attempt.quiz_open)

    async def test_receive(self):
        await self.connect()

        # Send a message to the websocket
        await self.communicator.send_to(json.dumps({"type": "start", "qid": self.quiz.id}))

        # Receive and decode the second message from the consumer
        response = await self.communicator.receive_from()
        data = json.loads(response)

        # Check the contents of the message
        self.assertEqual(data, {"type": "first_section", "section_type": "end", "section": {}})

        # Disconnect from the websocket
        await self.communicator.disconnect()

        # TODO: To make your tests better, evaluate more of the expected contents (self.assertEqual etc.),
        #  but to do that u need to define the expected contents first, as in instantiate the necessary models.
        #  When using asserts its better to call the predefined values e.g. self.quiz.id instead of just the number
        #  of what's expected, so that the test is more robust and can be used in the future when the values change.

