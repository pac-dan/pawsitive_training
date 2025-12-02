from django.test import TestCase
from products.models import Product, ProductCategory


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
