import datetime

from django.utils import timezone

from polls.models import Question


def create_question(question_text, days, hours=0, minutes=0, seconds=0):
    """
    Create a question with the given 'question_text' and published with an offset in 'days', either negative for past questions or positive for the future questions.
    """
    time = timezone.now() + datetime.timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    )
    return Question.objects.create(question_text=question_text, pub_date=time)
