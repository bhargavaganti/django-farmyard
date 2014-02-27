"""
Test suite for tester app.
"""

from django.test import TestCase
from django.core.urlresolvers import resolve
from subscriptions.views import MailingListView

class PublishedListTest(TestCase):
    def test_root_url_resolves_to_published_list(self):
        found = resolve('/subscriptions/')
        self.assertEqual(found.__class__, MailingListView)
