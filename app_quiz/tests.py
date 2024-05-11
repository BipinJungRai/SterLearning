from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import *


# Set up a valid quiz
def create_quiz():
    q = Quiz(name = "Test Quiz",
             description = "A quiz to test with",
             pathway = "LOANS")
    q.save()
    q.full_clean()

    return q


# Tests for MCQs
class MultipleChoiceTest(TestCase):
    # Test two can't be at same position
    def test_unique_position(self):
        quiz = create_quiz()

        kwargs = {"title": "MCQ",
                  "quiz": quiz,
                  "position": 1,
                  "points": 25
                  }

        q = MultipleChoice(**kwargs)
        q.save()

        q = MultipleChoice(**kwargs)
        q.save()

        with self.assertRaises(ValidationError):
            q.full_clean()

    # A question can't have 2 correct answers
    def test_one_correct_answer(self):
        quiz = create_quiz()

        question = MultipleChoice(title = "MCQ",
                                  quiz = quiz,
                                  position = 1,
                                  points = 25)
        question.save()

        a = MultipleChoiceOptions(text = "Option A",
                                  correct = True,
                                  question = question)
        a.save()

        b = MultipleChoiceOptions(text = "Option B",
                                  correct = True,
                                  question = question)
        b.save()

        with self.assertRaises(ValidationError):
            a.full_clean()

        with self.assertRaises(ValidationError):
            b.full_clean()

    # Test a valid question
    def test_valid(self):
        quiz = create_quiz()

        question = MultipleChoice(title = "MCQ",
                                  quiz = quiz,
                                  position = 1,
                                  points = 25)
        question.save()

        a = MultipleChoiceOptions(text = "Option A",
                                  correct = True,
                                  question = question)
        a.save()

        b = MultipleChoiceOptions(text = "Option B",
                                  correct = False,
                                  question = question)
        b.save()

        question.full_clean()
        a.full_clean()
        b.full_clean()


# Tests for FIBs
class FillInBlankTest(TestCase):
    # Test two can't be at same position
    def test_unique_position(self):
        quiz = create_quiz()

        kwargs = {"title": "FIB",
                  "quiz": quiz,
                  "position": 1
                  }

        q = FillInBlank(**kwargs)
        q.save()

        q = FillInBlank(**kwargs)
        q.save()

        with self.assertRaises(ValidationError):
            q.full_clean()

    # Test that sentence can't be empty
    def test_empty_sentence(self):
        quiz = create_quiz()

        question = FillInBlank(title = "FIB",
                               quiz = quiz,
                               position = 1)
        question.save()

        a = FillInBlankSentence(before = None,
                                blank = None,
                                after = None,
                                question = question,
                                points = 25)
        a.save()

        b = FillInBlankSentence(before = "",
                                blank = "",
                                after = "",
                                question = question,
                                points = 25)
        b.save()

        with self.assertRaises(ValidationError):
            a.full_clean()

        with self.assertRaises(ValidationError):
            b.full_clean()

    # Test valid
    def test_valid(self):
        quiz = create_quiz()

        question = FillInBlank(title = "FIB",
                               quiz = quiz,
                               position = 1)
        question.save()

        a = FillInBlankSentence(before = None,
                                blank = "Blank",
                                after = " and after",
                                question = question,
                                points = 25)
        a.save()

        b = FillInBlankSentence(before = "Before ",
                                blank = "blank",
                                after = " after",
                                question = question,
                                points = 25)
        b.save()

        question.full_clean()
        a.full_clean()
        b.full_clean()


# Tests for info sections
class InformationTest(TestCase):
    # Test two can't be at same position
    def test_unique_position(self):
        quiz = create_quiz()

        kwargs = {"title": "INF",
                  "quiz": quiz,
                  "position": 1,
                  "content": "Information section"
                  }

        i = Information(**kwargs)
        i.save()

        i = Information(**kwargs)
        i.save()

        with self.assertRaises(ValidationError):
            i.full_clean()

    # Test valid
    def test_valid(self):
        quiz = create_quiz()

        i = Information(title = "INF",
                        quiz = quiz,
                        position = 1,
                        content = "Information section")
        i.save()
        i.full_clean()
