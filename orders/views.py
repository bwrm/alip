from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from autoriz.models import MyUser
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


def order_create(request):
    # TODO: del email field for registered user
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                form.instance.user = MyUser.objects.get(email='anonymous@user.by')
            else:
                form.instance.user = request.user
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        if request.user.is_authenticated:
            data = {
                'first_name':request.user.first_name,
                'email':request.user.email,
                'address':request.user.location,
                'city':request.user.locality,
                'postal':request.user.postal_code,
                'phone_number':request.user.phone_number,
            }
            form = OrderCreateForm(data)
        else:
            form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})

class MyOrders(ListView, LoginRequiredMixin):
    model = Order
    template_name = 'orders/order/myorders.html'
    context_object_name = 'orders'
    #TODO: detail order list
    def get_queryset(self):
        order = OrderItem.objects.filter(order__user=self.request.user)
        return order

