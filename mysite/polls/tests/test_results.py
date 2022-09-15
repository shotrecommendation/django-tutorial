from django.test import TestCase
from django.urls import reverse

from .helper import create_question


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        Questions with pub_date set in the future should not be accessible. 404 error should emerge.
        """
        future_question = create_question("Future question.", days=10)
        response = self.client.get(reverse("polls:results", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Questions with pub_date in the past should be accessible through results view.
        """
        past_question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:results", args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)
