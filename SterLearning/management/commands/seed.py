# Import necessary models and functions
from django.core.management.base import BaseCommand
from app_quiz.models import Quiz, MultipleChoice, MultipleChoiceOptions, FillInBlank, FillInBlankSentence, Information

# Command class to seed the database
class Command(BaseCommand):
    help = 'Seed the database with sample quiz data'

    def handle(self, *args, **kwargs):
        # Delete preexisting data
        Quiz.objects.all().delete()

        # Create a sample quiz
        quiz = Quiz.objects.create(name='Sample Quiz', description='This is a sample quiz', pathway=Quiz.Pathways.LOANS)

        # Create sample multiple-choice questions
        mcq1 = MultipleChoice.objects.create(title='MCQ 1', quiz=quiz, position=1, points=10)
        mcq2 = MultipleChoice.objects.create(title='MCQ 2', quiz=quiz, position=2, points=20)

        # Create options for multiple-choice questions
        option1_mcq1 = MultipleChoiceOptions.objects.create(text='Option 1 for MCQ 1', correct=True, question=mcq1)
        option2_mcq1 = MultipleChoiceOptions.objects.create(text='Option 2 for MCQ 1', correct=False, question=mcq1)
        option1_mcq2 = MultipleChoiceOptions.objects.create(text='Option 1 for MCQ 2', correct=True, question=mcq2)
        option2_mcq2 = MultipleChoiceOptions.objects.create(text='Option 2 for MCQ 2', correct=False, question=mcq2)

        # Create sample fill-in-the-blank questions
        fib1 = FillInBlank.objects.create(title='FIB 1', quiz=quiz, position=3)
        fib2 = FillInBlank.objects.create(title='FIB 2', quiz=quiz, position=4)

        # Create sentences for fill-in-the-blank questions
        sentence1_fib1 = FillInBlankSentence.objects.create(before='This is ', blank='sample', after=' sentence.', question=fib1, points=5)
        sentence1_fib2 = FillInBlankSentence.objects.create(before='Another ', blank='example', after=' here.', question=fib2, points=5)

        # Create sample information screens
        info1 = Information.objects.create(title='Info 1', quiz=quiz, position=5, content='This is some information for the quiz.')
        info2 = Information.objects.create(title='Info 2', quiz=quiz, position=6, content='More information goes here.')

        self.stdout.write(self.style.SUCCESS('Sample quiz data seeded successfully.'))


