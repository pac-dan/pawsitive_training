from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile
from products.models import Product, ProductCategory
from orders.models import Order


class ProfileModelTest(TestCase):
    def test_profile_str(self):
        """
        Test the string representation of the Profile model by creating a user and profile.
        """
        user = User.objects.create(username="testuser")
        profile = Profile.objects.create(user=user, bio="Test bio")
        self.assertEqual(str(profile), "testuser's Profile")


class ProductModelTest(TestCase):
    def setUp(self):
        """
        Create a product category and product for testing.
        """
        self.category = ProductCategory.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            price="10.00",
            category=self.category,
            stock=5
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")


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
        """
        Test the string representation of the Order model.
        """
        expected_str = f"Order sess_123 for {self.user}"
        self.assertEqual(str(self.order), expected_str)
