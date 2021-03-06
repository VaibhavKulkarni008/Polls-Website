import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question


class QuestionsMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for question whose
        pub_date is in the future
        """
        future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for question whose pub_date
        is older than 1 day
        """
        old_question = Question(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for question whose pub_date
        is within the last day
        """
        recent_question = Question(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_question.was_published_recently(), True)


