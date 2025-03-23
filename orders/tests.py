from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order

class OrderModelTest(TestCase):
    def setUp(self):
        """
        Create a user and order to test the order model.
        """
        self.user = User.objects.create(username="testuser")
        self.order = Order.objects.create(
            user=self.user,
            stripe_checkout_session_id="sess_123",
            amount="50.00",
            status="pending"
        )
    
    def test_order_str(self):
        expected_str = f"Order sess_123 for {self.user}"
        self.assertEqual(str(self.order), expected_str)