from django.test import TestCase
from django.urls import reverse
from products.models import Product, ProductCategory
from django.conf import settings


class CheckoutViewTest(TestCase):
    def setUp(self):
        """
        Create a product and category to test the checkout view.
        """
        self.category = ProductCategory.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price="20.00",
            category=self.category,
            stock=10
        )

    def test_checkout_view_with_empty_basket(self):
        """
        Test the checkout view with an empty basket.
        """
        response = self.client.get(reverse('payments:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your basket is empty")

    def test_checkout_view_with_items(self):
        """
        Test the checkout view with items in the basket.
        """
        session = self.client.session
        session[settings.BASKET_SESSION_ID] = {
            str(self.product.id): {'quantity': 2, 'price': str(self.product.price)}
        }
        session.save()
        response = self.client.get(reverse('payments:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Total:")
