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
import requests
import io
import re
from urllib.parse import quote
from django.core.files.base import ContentFile


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


def curation_view(request):
    """Display all products from curation.csv for easy copying"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'curation.csv')
    products_list = []
    products_with_images = set(Product.objects.filter(image__isnull=False).values_list('id', flat=True))

    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['get_absolute_url'] = reverse('products:detail', args=[row['slug']])
                row['has_image'] = str(int(row['id']) in products_with_images)
                products_list.append(row)

    context = {
        'products': products_list,
        'total_count': len(products_list),
    }
    return render(request, 'products/curation.html', context)


@login_required
def upload_curation_image(request, product_id):
    """Handle image upload from curation page via click, drag-drop, or paste"""
    if request.method == 'POST' and request.FILES.get('image'):
        product = get_object_or_404(Product, id=product_id)
        product.image = request.FILES['image']
        product.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'image_url': product.image.url})
        messages.success(request, f'Image uploaded for {product.name}')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False}, status=400)
    return redirect('products:curation')


def curation_image_json(request, product_id):
    """Return image URL for a product (used by curation page to load existing images)"""
    product = get_object_or_404(Product, id=product_id)
    if product.image:
        return JsonResponse({'image_url': product.image.url})
    return JsonResponse({'image_url': None})


@login_required
def auto_fetch_image(request, product_id):
    """Auto-fetch product image from Google Images and save to product"""
    product = get_object_or_404(Product, id=product_id)
    query = f"{product.name} product"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Try DuckDuckGo image search first
        ddg_url = f"https://duckduckgo.com/?q={quote(query)}&iax=images&ia=images"
        resp = requests.get(ddg_url, headers=headers, timeout=10)

        if resp.status_code == 200:
            # Extract vqd token
            vqd_match = re.search(r'vqd=([\w-]+)&', resp.text)
            if vqd_match:
                vqd = vqd_match.group(1)
                api_url = f"https://duckduckgo.com/i.js?q={quote(query)}&vqd={vqd}&o=json"
                api_resp = requests.get(api_url, headers=headers, timeout=10)
                if api_resp.status_code == 200:
                    data = api_resp.json()
                    if data.get('results'):
                        img_url = data['results'][0]['image']
                        # Download the image
                        img_resp = requests.get(img_url, headers=headers, timeout=15)
                        if img_resp.status_code == 200:
                            ext = img_url.split('.')[-1].split('?')[0][:4]
                            if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                                ext = 'jpg'
                            filename = f"{product.slug}.{ext}"
                            product.image.save(filename, ContentFile(img_resp.content), save=True)
                            return JsonResponse({'success': True, 'image_url': product.image.url})

        # Fallback: try Google image search using a different approach
        google_url = f"https://www.google.com/search?q={quote(query)}&tbm=isch"
        g_resp = requests.get(google_url, headers=headers, timeout=10)
        if g_resp.status_code == 200:
            # Extract image URLs from the page
            img_matches = re.findall(r'\["(https?://[^"]+\.(?:jpg|jpeg|png|gif|webp)[^"]*)"', g_resp.text)
            if img_matches:
                img_url = img_matches[0].replace('\\u003d', '=').replace('\\u0026', '&').replace('\\/', '/')
                img_resp = requests.get(img_url, headers=headers, timeout=15)
                if img_resp.status_code == 200:
                    ext = img_url.split('.')[-1].split('?')[0][:4]
                    if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                        ext = 'jpg'
                    filename = f"{product.slug}.{ext}"
                    product.image.save(filename, ContentFile(img_resp.content), save=True)
                    return JsonResponse({'success': True, 'image_url': product.image.url})

        return JsonResponse({'success': False, 'error': 'No image found'}, status=404)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)