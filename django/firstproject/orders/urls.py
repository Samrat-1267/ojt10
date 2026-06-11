from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('review/', views.order_review, name='review'),
    path('complete/', views.order_complete, name='complete'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='confirmation'),
]
