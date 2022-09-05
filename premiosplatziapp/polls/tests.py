import datetime

from django.test import TestCase
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
        """test_was_published_recently_with_present_questions returns False for questions which pub_dates are in the present
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
