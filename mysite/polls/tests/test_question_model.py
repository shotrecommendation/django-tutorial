from django.test import TestCase
from django.urls import reverse

from .helper import create_question


class QuestionModelTests(TestCase):
    def test_was_published_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future
        """
        future_question = create_question("Future question.", days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than one day
        """
        old_question = create_question("Old question", days=-1, seconds=-1)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day
        """
        recent_question = create_question(
            "Recent question.", days=0, hours=-23, minutes=-59, seconds=-59
        )
        self.assertIs(recent_question.was_published_recently(), True)
