import datetime

from django.utils import timezone

from polls.models import Choice, Question


def create_question(
    question_text, days, hours=0, minutes=0, seconds=0, choices=("choice 1", "choice 2")
):
    """
    Create a question with the given 'question_text' and a set of 'choices'
    and published with an offset in 'days', either negative for past questions
    or positive for the future questions.
    """
    time = timezone.now() + datetime.timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    )
    question = Question.objects.create(question_text=question_text, pub_date=time)
    for choice in choices:
        Choice.objects.create(question=question, choice_text=choice)
    return question
