from django.db import models
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
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # save an empty basket in the session
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as modified to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
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
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]    
        self.save()