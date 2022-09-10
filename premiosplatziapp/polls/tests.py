import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question, Choice


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


def create_question(question_text: str, days: int):
    """create_question create_question Create a question with the given "question text", and published the given 
    number of days offset to now (negative for past questions, positive for questions to be published)

    Args:
        question_text (str): text of the question
        days (int): number of the days the question was published (in negative -) or is to be published (in positive +)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(choice_text: str, question, votes: int = 0):
    """create_choice _summary_

    Args:
        choice_text (str): text of the choice
        question (_type_): choice's question
        votes (int, optional): Votes of the choice. Defaults to 0.
    """
    return Choice.objects.create(choice_text=choice_text, question=question, votes=votes)


class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        """test_no_question If no question exist, an appropriate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
# * Challenge
    # def test_question_with_future_pub_date(self):
    #     """test_questions_with_future_pub_date Ensures there is no question with a greater pub_date than the current time
    #     """
    #     Question(
    #         question_text="Present Question", pub_date=timezone.now()).save()

    #     Question(
    #         question_text="Future Question", pub_date=timezone.now() + datetime.timedelta(days=30)).save()

    #     response = self.client.get(reverse("polls:index"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Present Question")
    #     self.assertNotContains(response, "Future Question")

    def test_future_question(self):
        """test_future_question Questions with a pub_date in the future are not displayed in the index page
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """test_past_question Questions with a pub_date in the past are displayed in the index page
        """
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [question])

    def test_future_and_past_question(self):
        """test_future_and_past_question Event if both past and future question exist, only past questions are displayed
        """
        past_question = create_question("Past question", days=-30)
        future_question = create_question("Future question", days=30)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_questions(self):
        """test_two_past_questions The questions index page may display multiple questions
        """
        past_question1 = create_question("Past question 1", days=-30)
        past_question2 = create_question("Past question 2", days=-40)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_questions(self):
        """test_two_future_questions The questions index page should display none future questions
        """
        future_question1 = create_question("Future question 1", days=30)
        future_question2 = create_question("Future question 2", days=40)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """test_future_question The detail view of a question with a pub_date in the future
        returns a 404 error not found
        """
        future_question = create_question("Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """test_past_question The detail view of a question with a pub_date in the past
        displays the question's text
        """
        past_question = create_question("Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_question_not_exists(self):
        """test_question_not_exists If question id does not exists, get 404 error
        """
        response = self.client.get(reverse("polls:results", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_display_question_choices_and_votes(self):
        """test_display_question_choices_and_votes Page may display votes 
        for every choice of a question
        """
        question = create_question("Question", -1)
        choice1 = create_choice("Choice 1", question=question, votes=1)
        choice2 = create_choice("Choice 2", question=question, votes=2)
        choice3 = create_choice("Choice 3", question=question)
        choice4 = create_choice("Choice 4", question=question)

        response = self.client.get(
            reverse("polls:results", kwargs={'pk': question.pk}))

        self.assertContains(response, question.question_text)
        self.assertContains(response, choice1.choice_text + ' -- ' + '1 vote')
        self.assertContains(response, choice2.choice_text + ' -- ' + '2 votes')
        self.assertContains(response, choice3.choice_text + ' -- ' + '0 votes')
        self.assertContains(response, choice4.choice_text + ' -- ' + '0 votes')
