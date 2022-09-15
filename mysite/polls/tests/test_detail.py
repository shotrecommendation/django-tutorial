from django.test import TestCase
from django.urls import reverse

from .helper import create_question


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with the pub_date in the future returns a 404 not found.
        """
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:detail", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:detail", args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)
