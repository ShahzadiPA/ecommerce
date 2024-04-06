from .models import Oncart,CartItem
from .views import _cart_id


def counter(request):
    item_count=0
    if 'admin' in request.path:
       return  {}
    else:
        try:
            cart=Oncart.objects.filter(carts_id=_cart_id(request))
            cart_items=CartItem.objects.all().filter(oncart=cart[:1])
            for cart_item in cart_items:
                 item_count += cart_item.quantity
        except Oncart.DoesNotExist:
            item_count =0
    return  dict(item_count=item_count)