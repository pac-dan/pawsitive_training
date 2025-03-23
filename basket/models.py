from decimal import Decimal
from django.conf import settings
from products.models import Product


# The Basket class is a simple container that allows us to manage a basket in the session.
# It is initialized with a request object and retrieves the current basket from the session.
# The basket is stored as a dictionary in the session using the BASKET_SESSION_ID key.
# If the basket does not exist in the session, an empty dictionary is saved in the session.
# The basket attribute is a reference to the dictionary stored in the session.
# This allows us to easily add, remove, and update items in the basket.

class Basket:
    """
    A shopping basket class that allows us to manage the items in the basket by adding, removing, and updating products.
    """
    def __init__(self, request):
        """
        Initialize the basket object and get the current basket from the session.
        """
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # save an empty basket in the session
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the basket or update its quantity
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Save the basket in the session
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the basket
        """
        product_id = str(product.id)
        if product_id in self.basket:
            # if more than 1 quantity, reduce the quantity
            if self.basket[product_id]['quantity'] > 1:
                self.basket[product_id]['quantity'] -= 1
            else:
                # otherwise, remove the item from the basket
                del self.basket[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the basket and get the products from the database.
        """
        product_ids = self.basket.keys()
        # get the product objects and add them to the basket
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.basket[str(product.id)]['product'] = product

        for item in self.basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        
    def __len__(self):
        """
        Count all items in the basket
        """
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        """
        Calculate the total cost of the items in the basket.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def clear(self):
        """
        Remove the basket from the session
        """
        del self.session[settings.BASKET_SESSION_ID]    
        self.save()