from django.shortcuts import render
from products.models import Product, Category, Review


def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    best_sellers = Product.objects.filter(is_best_seller=True, is_active=True)[:8]
    categories = Category.objects.filter(parent__isnull=True)
    component_categories = Category.objects.filter(is_component_category=True)
    reviews = Review.objects.all().select_related('user', 'product')[:6]
    custom_builds = Product.objects.filter(is_custom_build=True, is_active=True)[:4]

    context = {
        'featured_products': featured_products,
        'best_sellers': best_sellers,
        'categories': categories,
        'component_categories': component_categories,
        'reviews': reviews,
        'custom_builds': custom_builds,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'myapp/about.html')


def profile(request):
    return render(request, 'myapp/profile.html')
