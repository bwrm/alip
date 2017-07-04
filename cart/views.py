from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main_site.models import Product, DetailProduce, OurProfit
from .cart import Cart
from .forms import CartAddProductForm
from main_site.views import Prices

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    endprice = Prices()
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 price=endprice.get_end_price(product_id),
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_remove_all(request):
    cart = Cart(request)
    cart.remove_all()
    return redirect('cart:cart_detail')



def cart_detail(request):
    cart = Cart(request)
    total_price = 0
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'],
                                                                   'price':item['price'],
                                                                   'update':True})
        total_price += item['quantity']*item['price']
    return render(request, 'cart/detail.html', {'cart':cart, 'total_price':total_price})