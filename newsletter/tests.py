from django.test import TestCase


class NewsletterTestCase(TestCase):
    """Basic test cases for newsletter functionality"""

    def test_newsletter_app_exists(self):
        """Test that newsletter app is properly configured"""
        from newsletter.models import NewsletterSubscriber
        self.assertTrue(NewsletterSubscriber)

    def test_newsletter_form_exists(self):
        """Test that newsletter form is accessible"""
        from newsletter.forms import NewsletterSignupForm
        self.assertTrue(NewsletterSignupForm)
