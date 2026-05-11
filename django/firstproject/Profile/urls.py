from django.urls import path
from . import views

urlpatterns = [
    path('Profile/', views.profile, name='profile'),
] 