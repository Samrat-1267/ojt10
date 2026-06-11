from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from .models import Category, Product, Review
from .forms import ReviewForm


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(parent__isnull=True)
    selected_category = request.GET.get('category')
    sort = request.GET.get('sort', '-created_at')
    q = request.GET.get('q', '')

    if selected_category:
        try:
            cat = Category.objects.get(slug=selected_category)
            child_slugs = list(cat.children.values_list('slug', flat=True))
            if child_slugs:
                products = products.filter(category__slug__in=child_slugs)
            else:
                products = products.filter(category__slug=selected_category)
        except Category.DoesNotExist:
            products = products.filter(category__slug=selected_category)

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    valid_sorts = {
        'price': 'price',
        '-price': '-price',
        'name': 'name',
        '-name': '-name',
        'rating': '-rating_avg',
        '-created_at': '-created_at',
        'created_at': 'created_at',
    }
    if sort in valid_sorts and sort != 'rating' and sort != '-rating':
        products = products.order_by(sort)
    elif sort == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'current_sort': sort,
        'query': q,
    }
    return render(request, 'products/product_list.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    child_categories = category.children.all()

    sort = request.GET.get('sort', '-created_at')
    if sort in ['price', '-price', 'name', '-name', '-created_at', 'created_at']:
        products = products.order_by(sort)

    context = {
        'products': products,
        'category': category,
        'child_categories': child_categories,
        'current_sort': sort,
    }
    return render(request, 'products/category_products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    review_form = ReviewForm()

    context = {
        'product': product,
        'related_products': related_products,
        'review_form': review_form,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            if Review.objects.filter(product=product, user=request.user).exists():
                messages.error(request, 'You have already reviewed this product.')
                return redirect('products:detail', slug=slug)
            review.save()
            messages.success(request, 'Your review has been added.')
    return redirect('products:detail', slug=slug)
