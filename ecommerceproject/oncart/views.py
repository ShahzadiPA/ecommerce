from django.shortcuts import render, redirect, get_object_or_404
from bcart.models import Product
from .models import Oncart, CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    oncart = request.session.session_key
    if not oncart:
        oncart = request.session.create()
    return oncart


def add_cart(request, product_id):
    products = Product.objects.get(id=product_id)
    try:
        oncart = Oncart.objects.get(carts_id=_cart_id(request))
    except Oncart.DoesNotExist:
        oncart = Oncart.objects.create(carts_id=_cart_id(request)
                                       )
        oncart.save(),
    try:
        cart_item = CartItem.objects.get(products=products, oncart=oncart)
        if cart_item.quantity < cart_item.products.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            products=products,
            quantity=1,
            oncart=oncart
        )
        cart_item.save()
    return redirect('oncart:cart_details')


def cart_details(request, total=0, counter=0, cart_items=None):
    try:
        oncart = Oncart.objects.get(carts_id=_cart_id(request))
        cart_items = CartItem.objects.filter(oncart=oncart, active=True)
        for cart_item in cart_items:
            total += (cart_item.products.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def cart_remove(request, product_id):
    oncart = Oncart.objects.get(carts_id=_cart_id(request))
    products = get_object_or_404(Product, id=product_id)
    cart_items = CartItem.objects.get(products=products, oncart=oncart)
    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
    else:
        cart_items.delete()
    return redirect('oncart:cart_details')
def full_remove(request,product_id):
    oncart = Oncart.objects.get(carts_id=_cart_id(request))
    products = get_object_or_404(Product, id=product_id)
    cart_items = CartItem.objects.get(products=products, oncart=oncart)
    cart_items.delete()
    return redirect('oncart:cart_details')

