from django.urls import path
from . import views

urlpatterns=[
    path('',views.home2,name='home2'),
]