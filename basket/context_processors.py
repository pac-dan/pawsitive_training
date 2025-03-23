from .models import Basket  

def basket_total(request):
    """
    A context processor to add the basket total to the context.
    """
    basket = Basket(request)
    
    return {
        'grand_total': basket.get_total_price(),
        'basket_total': len(basket)
    }