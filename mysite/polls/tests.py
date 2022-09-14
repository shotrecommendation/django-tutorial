import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days_from_now):
    """
    Create a question with the given 'question_text' and published with an offset in 'days_from_now', either negative for past questions or positive for the future questions.
    """
    time = timezone.now() + datetime.timedelta(days=days_from_now)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with pub_date in the past should be displayed.
        """
        past_question = create_question(
            question_text="Past question", days_from_now=-30
        )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_future_question(self):
        """
        Questions with pub_date in the future should not be displayed.
        """
        create_question(question_text="Future question.", days_from_now=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if past and future questions exist, only past questions should be displayed.
        """
        past_question = create_question(
            question_text="Past question", days_from_now=-30
        )
        create_question(question_text="Future question.", days_from_now=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_two_past_questions(self):
        """
        The question index page can display multiple questions.
        """
        past_question_1 = create_question(
            question_text="Past question 1.", days_from_now=-20
        )
        past_question_2 = create_question(
            question_text="Past question 2.", days_from_now=-10
        )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question_2, past_question_1]
        )


class QuestionModelTests(TestCase):
    def test_was_published_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than one day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
