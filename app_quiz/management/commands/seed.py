import json

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile

from app_quiz.models import Quiz, MultipleChoice, MultipleChoiceOptions, FillInBlank, FillInBlankSentence, \
    Information
from app_user.models import Avatar, Decoration


# Define a custom management command for Django
class Command(BaseCommand):
    # Provide a description for the command
    help = 'Load a seed data from a JSON file'

    # The handle method is the main logic of the command
    def handle(self, *args, **options):
        # Delete all existing data in the models
        Quiz.objects.all().delete()
        MultipleChoice.objects.all().delete()
        MultipleChoiceOptions.objects.all().delete()
        FillInBlank.objects.all().delete()
        FillInBlankSentence.objects.all().delete()
        Information.objects.all().delete()
        Avatar.objects.all().delete()
        Decoration.objects.all().delete()

        # Seed all the profile avatars and decorations
        avatar = Avatar(name = 'Cat',
                        image = ImageFile(open('sample_data/icon-avatar-cat.png', 'rb'),
                                        name='icon-avatar-cat.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Dog',
                        image = ImageFile(open('sample_data/icon-avatar-dog.png', 'rb'),
                                        name='icon-avatar-dog.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Duck',
                        image = ImageFile(open('sample_data/icon-avatar-duck.png', 'rb'),
                                        name='icon-avatar-duck.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Lily',
                        image = ImageFile(open('sample_data/icon-avatar-lily.png', 'rb'),
                                        name='icon-avatar-lily.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Snail',
                        image = ImageFile(open('sample_data/icon-avatar-snail.png', 'rb'),
                                        name='icon-avatar-snail.png'))
        avatar.save()
        avatar.full_clean()

        decoration = Decoration(name = 'Crown',
                                image = ImageFile(open('sample_data/icon-hat-crown.png', 'rb'),
                                        name='icon-hat-crown.png'))
        decoration.save()
        decoration.full_clean()

        decoration = Decoration(name = 'Propellor Hat',
                                image = ImageFile(open('sample_data/icon-hat-propellor.png', 'rb'),
                                        name='icon-hat-propellor.png'))
        decoration.save()
        decoration.full_clean()

        decoration = Decoration(name = 'Wizard Hat',
                                image = ImageFile(open('sample_data/icon-hat-wizard.png', 'rb'),
                                        name='icon-hat-wizard.png'))
        decoration.save()
        decoration.full_clean()

        # Open the JSON file containing the seed data
        with open('app_quiz/management/commands/sample_data.json', 'r') as file:
            # Load the JSON data
            data = json.load(file)

        # Iterate over each quiz in the data
        for quiz_data in data['quizzes']:
            # Create a new Quiz object for each quiz in the data
            quiz = Quiz.objects.create(
                name=quiz_data['name'],
                description=quiz_data['description'],
                pathway=quiz_data['pathway']
            )

            # Iterate over each section in the quiz
            for section_data in quiz_data['sections']:
                # Check the type of the section and create the appropriate object
                if section_data['type'] == 'MultipleChoice':
                    section = MultipleChoice.objects.create(
                        title=section_data['title'],
                        quiz=quiz,
                        position=section_data['position'],
                        points=section_data['points']
                    )

                    # Create a MultipleChoiceOptions object for each option in the section
                    for option_data in section_data['options']:
                        MultipleChoiceOptions.objects.create(
                            text=option_data['text'],
                            correct=option_data['correct'],
                            question=section
                        )

                elif section_data['type'] == 'FillInBlank':
                    section = FillInBlank.objects.create(
                        title=section_data['title'],
                        quiz=quiz,
                        position=section_data['position']
                    )

                    # Create a FillInBlankSentence object for each sentence in the section
                    for sentence_data in section_data['sentences']:
                        FillInBlankSentence.objects.create(
                            before=sentence_data['before'],
                            blank=sentence_data['blank'],
                            after=sentence_data['after'],
                            question=section,
                            points=sentence_data['points']
                        )

                elif section_data['type'] == 'Information':
                    # Create an Information object for the section
                    Information.objects.create(
                        title=section_data['title'],
                        quiz=quiz,
                        position=section_data['position'],
                        content=section_data['content']
                    )

        # Print a success message when the data is loaded
        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
