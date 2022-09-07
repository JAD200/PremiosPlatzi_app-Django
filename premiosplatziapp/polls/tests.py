import datetime
from urllib import response

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


# Models tests
class QuestionModelTests(TestCase):

    def setUp(self) -> None:
        self.question = Question(
            question_text="¿Quien es el mejor CD de Platzi?")

    def test_was_published_recently_with_future_questions(self):
        """test_was_published_recently_with_future_questions returns False for questions which pub_dates are in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        """test_was_published_recently_with_present_questions returns True for questions which pub_dates are in the present
        """
        time = timezone.now() - datetime.timedelta(hours=23)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self):
        """test_was_published_recently_with_past_questions returns False for questions which pub_dates are in the past
        """
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)


# Views tests

class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        """test_no_question If no question exist, an appropriate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_questions_with_future_pub_date(self):
        """test_questions_with_future_pub_date Ensures there is no question with a greater pub_date than the current time
        """
        Question(
            question_text="Present Question", pub_date=timezone.now()).save()

        Question(
            question_text="Future Question",pub_date=timezone.now() + datetime.timedelta(days=30)).save()

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Present Question")
        self.assertNotContains(response, "Future Question")
