from django.test import TestCase, RequestFactory
from products.models import Product, ProductCategory
from basket import Basket

class BasketTest(TestCase):
    def setUp(self):
        """
        Create a product category and product for testing.
        """
        self.factory = RequestFactory()
        self.category = ProductCategory.objects.create(name="Category Test")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test product description",
            price="15.00",
            category=self.category,
            stock=10
        )
    
    def test_add_to_basket(self):
        """
        Test adding a product to the basket.
        """
        request = self.factory.get('/')
        request.session = {}
        basket = Basket(request)
        basket.add(product=self.product, quantity=2, update_quantity=False)
        self.assertIn(str(self.product.id), basket.basket)
        self.assertEqual(basket.basket[str(self.product.id)]['quantity'], 2)
    
    def test_remove_from_basket(self):
        """
        Test removing a product from the basket.
        """
        request = self.factory.get('/')
        request.session = {}
        basket = Basket(request)
        basket.add(product=self.product, quantity=2, update_quantity=False)
        basket.remove(self.product)
        self.assertEqual(basket.basket[str(self.product.id)]['quantity'], 1)
