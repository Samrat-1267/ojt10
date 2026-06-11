from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.models import Cart
from cart.views import get_cart


@login_required
def checkout(request):
    cart = get_cart(request)
    if cart.item_count == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('products:list')

    shipping_cost = 9.99 if cart.subtotal < 100 else 0

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.session['checkout_data'] = form.cleaned_data
            return redirect('orders:review')
    else:
        initial = {}
        default_address = request.user.addresses.filter(is_default=True).first()
        if default_address:
            initial = {
                'shipping_name': default_address.full_name,
                'shipping_address': default_address.address_line1,
                'shipping_address2': default_address.address_line2,
                'shipping_city': default_address.city,
                'shipping_state': default_address.state,
                'shipping_postal_code': default_address.postal_code,
                'shipping_country': default_address.country,
                'phone': default_address.phone,
            }
        if request.user.email:
            initial['email'] = request.user.email
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'shipping_cost': shipping_cost,
    })


@login_required
def order_review(request):
    checkout_data = request.session.get('checkout_data')
    if not checkout_data:
        return redirect('orders:checkout')

    cart = get_cart(request)
    shipping_cost = 9.99 if cart.subtotal < 100 else 0
    subtotal = cart.subtotal
    total = subtotal + shipping_cost

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            email=checkout_data['email'],
            phone=checkout_data['phone'],
            shipping_name=checkout_data['shipping_name'],
            shipping_address=checkout_data['shipping_address'],
            shipping_address2=checkout_data.get('shipping_address2', ''),
            shipping_city=checkout_data['shipping_city'],
            shipping_state=checkout_data['shipping_state'],
            shipping_postal_code=checkout_data['shipping_postal_code'],
            shipping_country=checkout_data['shipping_country'],
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            discount=0,
            total=total,
            notes=checkout_data.get('notes', ''),
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                custom_build_data=item.custom_build_data,
            )

        cart.delete()
        del request.session['checkout_data']
        messages.success(request, 'Order placed successfully!')
        return redirect('orders:confirmation', order_id=order.id)

    return render(request, 'orders/review.html', {
        'checkout_data': checkout_data,
        'cart': cart,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    })


@login_required
def order_complete(request):
    return redirect('orders:confirmation', order_id=0)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})
