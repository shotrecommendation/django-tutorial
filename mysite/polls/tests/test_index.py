from django.test import TestCase
from django.urls import reverse

from .helper import create_question


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
        past_question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_future_question(self):
        """
        Questions with pub_date in the future should not be displayed.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if past and future questions exist, only past questions should be displayed.
        """
        past_question = create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_two_past_questions(self):
        """
        The question index page can display multiple questions.
        """
        past_question_1 = create_question(question_text="Past question 1.", days=-20)
        past_question_2 = create_question(question_text="Past question 2.", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question_2, past_question_1]
        )
