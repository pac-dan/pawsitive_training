from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from products.models import Product, ProductCategory
from basket.models import Basket


class BasketTest(TestCase):
    def setUp(self):
        """
        Create a product category and product for testing.
        """
        self.factory = RequestFactory()
        self.category = ProductCategory.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test product description",
            price="15.00",
            category=self.category,
            stock=10
        )

    def create_request_with_session(self):
        """
        Create a request with a proper session.
        """
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_add_to_basket(self):
        """
        Test adding a product to the basket.
        """
        request = self.create_request_with_session()
        basket = Basket(request)
        basket.add(product=self.product, quantity=2, update_quantity=False)
        self.assertIn(str(self.product.id), basket.basket)
        self.assertEqual(basket.basket[str(self.product.id)]['quantity'], 2)

    def test_remove_from_basket(self):
        """
        Test removing a product from the basket.
        """
        request = self.create_request_with_session()
        basket = Basket(request)
        basket.add(product=self.product, quantity=2, update_quantity=False)
        basket.remove(self.product)
        self.assertEqual(basket.basket[str(self.product.id)]['quantity'], 1)

    def test_update_quantity(self):
        """
        Test updating the quantity of a product in the basket.
        """
        request = self.create_request_with_session()
        basket = Basket(request)
        basket.add(product=self.product, quantity=1, update_quantity=False)
        basket.add(product=self.product, quantity=3, update_quantity=True)
        self.assertEqual(basket.basket[str(self.product.id)]['quantity'], 3)

    def test_basket_total_price(self):
        """
        Test calculating the total price of the basket.
        """
        request = self.create_request_with_session()
        basket = Basket(request)
        basket.add(product=self.product, quantity=2, update_quantity=False)
        expected_total = Decimal(self.product.price) * 2
        self.assertEqual(basket.get_total_price(), expected_total)

    def test_basket_length(self):
        """
        Test counting items in the basket.
        """
        request = self.create_request_with_session()
        basket = Basket(request)
        basket.add(product=self.product, quantity=3, update_quantity=False)
        self.assertEqual(len(basket), 3)
