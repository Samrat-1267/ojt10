from django.urls import path
from . import views

app_name = 'custom_pc_builder'

urlpatterns = [
    path('', views.builder, name='builder'),
    path('api/components/<str:component_type>/', views.get_components, name='get_components'),
    path('api/check-compatibility/', views.check_compatibility, name='check_compatibility'),
    path('save/', views.save_build, name='save'),
    path('load/<int:build_id>/', views.load_build, name='load'),
    path('delete/<int:build_id>/', views.delete_build, name='delete'),
]
