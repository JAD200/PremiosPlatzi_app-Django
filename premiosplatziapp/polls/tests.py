import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


# Models tests
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """test_was_published_recently_with_future_questions returns False for questions which pub_dates are in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


# Views tests
