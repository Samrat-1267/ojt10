from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('category/<slug:slug>/', views.category_products, name='category'),
    path('curation/', views.curation_view, name='curation'),
    path('curation-image/<int:product_id>/', views.curation_image_json, name='curation_image_json'),
    path('upload-curation-image/<int:product_id>/', views.upload_curation_image, name='upload_curation_image'),
    path('auto-fetch-image/<int:product_id>/', views.auto_fetch_image, name='auto_fetch_image'),
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('<slug:slug>/add-review/', views.add_review, name='add_review'),
]
