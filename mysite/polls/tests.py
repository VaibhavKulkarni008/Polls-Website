import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question


class QuestionsMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for question whose
        pub_date is in the future
        """
        future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for question whose pub_date
        is older than 1 day
        """
        old_question = Question(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return True for question whose pub_date
        is within the last day
        """
        recent_question = Question(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_question.was_published_recently(), True)


def create_question(question, days):
    """
    Creates a poll with the given `question` published the given number of
    `days` offset to now (negative for question published in the past,
    positive for question that have yet to be published).
    """
    return Question.objects.create(
        question_text=question,
        pub_date=timezone.now() + datetime.timedelta(days=days)
    )


class IndexViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no question exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questionss with a pub_date in the past should be displayed on the index page.
        """
        create_question(question="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Question poll.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questionss with a pub_date in the future should not be displayed on the
        index page.
        """
        create_question(question="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No questions are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions should be
        displayed.
        """
        create_question(question="Past question.", days=-30)
        create_question(question="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Questions: Past question.>']
        )

    def test_index_view_with_two_past_question(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question="Past question 1.", days=-30)
        create_question(question="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Questions: Past question 2.>', '<Questions: Past question 1.>']
        )


class QuestionsIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a poll with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question='Future question.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_question = create_question(question='Past Questions.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)