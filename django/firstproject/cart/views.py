from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart


def cart_detail(request):
    cart = get_cart(request)
    context = {
        'cart': cart,
        'shipping': 9.99 if cart.subtotal < 100 else 0,
    }
    return render(request, 'cart/cart_detail.html', context)


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 0}
    )

    quantity = int(request.POST.get('quantity', 1))
    cart_item.quantity += quantity
    if cart_item.quantity > product.stock:
        cart_item.quantity = product.stock
        messages.warning(request, f'Only {product.stock} available.')
    cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'item_count': cart.total_items,
            'subtotal': str(cart.subtotal),
        })

    messages.success(request, f'{product.name} added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'products:list'))


def cart_remove(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:detail')


def cart_update(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            if quantity > item.product.stock:
                quantity = item.product.stock
                messages.warning(request, f'Only {item.product.stock} available.')
            item.quantity = quantity
            item.save()
            messages.success(request, 'Cart updated.')

    return redirect('cart:detail')
