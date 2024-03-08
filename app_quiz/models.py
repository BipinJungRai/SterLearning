from django.db import models
from django.utils.translation import gettext


# Quiz model - stores which pathway the quiz is in and its name.
class Quiz(models.Model):
    class Pathways(models.TextChoices):
        LOANS = "LOANS", gettext("LoansPathway")
        BUDGET = "BUDGET", gettext("BudgetingPathway")
        BANK = "BANK", gettext("BankAccountsPathway")
        TAX = "TAX", gettext("TaxesPathway")
        PENSION = "PENSION", gettext("PensionsPathway")

    name = models.CharField(max_length = 250)
    pathway = models.CharField(choices = Pathways.choices)


# Abstract class for a section within a quiz containing a title and position.
class QuizSection(models.Model):
    title = models.CharField()
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)
    position = models.IntegerField()

    class Meta:
        abstract = True


# Multiple choice question, stores points awarded for correct answer.
class MultipleChoice(QuizSection):
    points = models.IntegerField()


# Option for a MCQ. Relates to one MultipleChoice instance.
class MultipleChoiceOptions(models.Model):
    text = models.CharField()
    correct = models.BooleanField()
    question = models.ForeignKey(MultipleChoice, on_delete = models.CASCADE)

# Model for fill in the blank questions. No additional fields needed.
class FillInBlank(QuizSection):
    pass


# A setence within a fill in the blank question. Blank can be at the start or
# end and is optional. Related to one FillInBlank.
class FillInBlankSentence(models.Model):
    before = models.CharField(null = True)
    blank = models.CharField(null = True)
    after = models.CharField(null = True)
    question = models.ForeignKey(FillInBlank, on_delete = models.CASCADE)
    points = models.IntegerField()


# Model for an information screen that can be put in a quiz to give user info.
class Information(QuizSection):
    content = models.TextField()
