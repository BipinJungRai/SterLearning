from django.core.management.base import BaseCommand
from app_quiz.models import *


class Command(BaseCommand):
    # TEMPORARY SEEDING FOR QUIZ TESTING
    def handle(self, *args, **kwargs):
        Quiz.objects.all().delete()

        kwargs = {"name": "mortgages",
                    "description": "mortgages are expensive",
                    "pathway": "LOANS"}
        
        quiz = Quiz(**kwargs)
        quiz.save()

        kwargs = {"title": "info about mortgages",
                  "quiz": quiz,
                  "position": 1,
                  "content": "they big exponse"}
        
        info = Information(**kwargs)
        info.save()

        kwargs = {"title": "mcq about mortgages",
                  "quiz": quiz,
                  "position": 2,
                  "points": 50}
        
        mcq = MultipleChoice(**kwargs)
        mcq.save()

        kwargs = {"text": "option a",
                  "correct": True, 
                  "question": mcq}
        
        a = MultipleChoiceOptions(**kwargs)
        a.save()

        kwargs = {"text": "option b",
                  "correct": False, 
                  "question": mcq}
        
        b = MultipleChoiceOptions(**kwargs)
        b.save()

        kwargs = {"title": "fib about mortgages",
                  "quiz": quiz,
                  "position": 3}

        fib = FillInBlank(**kwargs)
        fib.save()

        kwargs = {"before": "hello ",
                  "blank": "there",
                  "after": None,
                  "question": fib,
                  "points": 50}
        
        s = FillInBlankSentence(**kwargs)
        s.save()

        kwargs = {"before": "general ",
                  "blank": "kenobi",
                  "after": ", you are a bold one",
                  "question": fib,
                  "points": 50}
        
        s = FillInBlankSentence(**kwargs)
        s.save()
