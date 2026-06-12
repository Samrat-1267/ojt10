from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.urls import reverse
from django.http import JsonResponse
from .models import Category, Product, Review
from .forms import ReviewForm
import csv
import os


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
        '-created_at': '-created_at',
        'created_at': 'created_at',
    }
    if sort in valid_sorts:
        products = products.order_by(valid_sorts[sort])
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


def curation_view(request):
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'curation.csv')
    products_list = []

    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['get_absolute_url'] = reverse('products:detail', args=[row['slug']])
                products_list.append(row)

    for p in products_list:
        pid = int(p['id'])
        try:
            product = Product.objects.get(id=pid)
            if product.image and product.image.name:
                p['has_image'] = True
                p['image_url'] = product.image.url
            else:
                p['has_image'] = False
                p['image_url'] = ''
        except Product.DoesNotExist:
            p['has_image'] = False
            p['image_url'] = ''

    return render(request, 'products/curation.html', {'products': products_list, 'total_count': len(products_list)})


def upload_curation_image(request, product_id):
    if request.method == 'POST' and request.FILES.get('image'):
        product = get_object_or_404(Product, id=product_id)
        product.image = request.FILES['image']
        product.save()
        messages.success(request, f'Image saved for {product.name}')
    return redirect('products:curation')
