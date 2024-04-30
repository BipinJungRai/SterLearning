import json
import os

from django.core.management.base import BaseCommand
from app_quiz.models import Quiz, MultipleChoice, MultipleChoiceOptions, FillInBlank, FillInBlankSentence

class Command(BaseCommand):
    """Django command to load data from JSON files into the Quiz model."""

    help = 'Load data from JSON files into the Quiz model'

    def handle(self, *args, **options):
        """Handle the command."""

        # Define the paths to the JSON files
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        payslips_and_taxes_quiz_json = os.path.join(base_dir, 'payslips_taxes_data.json')
        budgeting_quiz_json = os.path.join(base_dir, 'budget_data.json')

        # Load Payslips and Taxes Quiz data
        with open(payslips_and_taxes_quiz_json, 'r') as f:
            payslips_and_taxes_quiz_data = json.load(f)

        # Load Budgeting Quiz data
        with open(budgeting_quiz_json, 'r') as f:
            budgeting_quiz_data = json.load(f)

        # Delete existing data
        Quiz.objects.all().delete()
        MultipleChoice.objects.all().delete()
        MultipleChoiceOptions.objects.all().delete()
        FillInBlank.objects.all().delete()
        FillInBlankSentence.objects.all().delete()

        # Seed data for Payslips and Taxes Quiz
        self.seed_quiz_data(payslips_and_taxes_quiz_data)
        self.stdout.write(self.style.SUCCESS('Data for Payslips and Taxes Quiz loaded successfully!'))

        # Seed data for Budgeting Quiz
        self.seed_quiz_data(budgeting_quiz_data)
        self.stdout.write(self.style.SUCCESS('Data for Budgeting Quiz loaded successfully!'))

    def seed_quiz_data(self, quiz_data):
        """Seeds data for a single quiz."""

        quiz = Quiz.objects.create(
            name=quiz_data['name'],
            description=quiz_data['description'],
            pathway=quiz_data['pathway']
        )

        # Loop through each section in the quiz data
        for section_data in quiz_data['sections']:
            # Loop through each question in the section
            for question_data in section_data['questions']:
                if question_data['type'] == 'Multiple Choice':
                    # Create a new MultipleChoice question
                    question = MultipleChoice.objects.create(
                        title=question_data['question'],  # Used 'question' from JSON as 'title'
                        quiz=quiz,
                        position=section_data['position'],
                        points=question_data['points']
                    )

                    # Loop through each option for the question
                    for option_text in question_data['options']:
                        # Check if the option is the correct answer
                        correct = option_text == question_data['correct_option']
                        # Create a new MultipleChoiceOptions object for the option
                        MultipleChoiceOptions.objects.create(
                            text=option_text,
                            correct=correct,
                            question=question
                        )
                elif question_data['type'] == 'Fill in the Blank':
                    # Create a new FillInBlank question
                    question = FillInBlank.objects.create(
                        title=question_data['question'],  # Used 'question' from JSON as 'title'
                        quiz=quiz,
                        position=section_data['position']
                    )

                    # Create a new FillInBlankSentence object for the question
                    FillInBlankSentence.objects.create(
                        before=question_data['before'],
                        blank=question_data['blank'],
                        after=question_data['after'],
                        question=question,
                        points=question_data['points']
                    )