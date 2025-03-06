from .models import Basket  

def basket_total(request):
    basket = Basket(request)
    
    return {
        'grand_total': basket.get_total_price(),
        'basket_total': len(basket)
    }