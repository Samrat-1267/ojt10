from django.shortcuts import render
from products.models import Category, Review


def home(request):
    categories = Category.objects.filter(parent__isnull=True)
    reviews = Review.objects.all().select_related('user', 'product')[:6]
    context = {
        'categories': categories,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'myapp/about.html')


def profile(request):
    return render(request, 'myapp/profile.html')
