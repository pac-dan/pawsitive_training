from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, ProductCategory
from subscriptions.models import Subscription

class ProductsDisplayViewTest(TestCase):
    def setUp(self):
        """
        Create a product category and 10 products for testing.
        """
        self.category = ProductCategory.objects.create(name="Category Test")
        for i in range(10):
            Product.objects.create(
                name=f"Product {i}",
                description="Test Description",
                price="10.00",
                category=self.category,
                stock=10
            )
    
    def test_products_display_status_code(self):   
        """
        Test the products display view status code.
        """
        response = self.client.get(reverse('products:products_display'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products_display.html")
    
    def test_products_display_pagination(self):
        """
        Test the products display view pagination.
        """
        response = self.client.get(reverse('products:products_display') + "?page=1")
        self.assertIn('page_obj', response.context)


class SubscriptionViewTest(TestCase):
    def setUp(self):
        """
        Create a user and log in for testing.
        """
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
    
    def test_subscription_dashboard_no_subscription(self):
        """
        Test the subscription dashboard with no subscription.
        """
        response = self.client.get(reverse('subscriptions:subscribe'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You don't have a subscription yet")
    
    def test_subscription_dashboard_active_subscription(self):
        """
        Test the subscription dashboard with an active subscription.
        """
        sub = Subscription.objects.create(
            user=self.user,
            subscription_type="monthly",
            active=True,
            expiry_date="2100-01-01"  
        )
        response = self.client.get(reverse('subscriptions:subscribe'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "active")


class ProductDetailViewTest(TestCase):
    def setUp(self):
        """
        Create a product category and product for testing.
        """
        self.category = ProductCategory.objects.create(name="Category Test")
        self.product = Product.objects.create(
            name="Test Product",
            description="Product detail test",
            price="15.00",
            category=self.category,
            stock=5
        )
    
    def test_product_detail_status_code(self):
        """
        Test the product detail view status code.
        """
        url = reverse('products:product_detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)