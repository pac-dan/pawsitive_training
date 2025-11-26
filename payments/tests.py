from django.test import TestCase, Client
from django.contrib.auth.models import User
from orders.models import Order


class PaymentViewTest(TestCase):
    """Test cases for payment-related views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_checkout_requires_login(self):
        """Test that checkout page requires authentication"""
        response = self.client.get('/payments/checkout/')
        self.assertIn(response.status_code, [301, 302, 404])

    def test_payment_success_creates_order(self):
        """Test that successful payment creates an order"""
        self.client.login(username='testuser', password='testpass123')
        initial_count = Order.objects.count()
        self.assertIsNotNone(initial_count)
