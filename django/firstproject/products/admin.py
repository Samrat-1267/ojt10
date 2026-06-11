from django.contrib import admin
from .models import Category, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['user', 'rating', 'comment']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_component_category', 'order']
    list_filter = ['is_component_category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_featured', 'is_best_seller', 'is_active']
    list_filter = ['category', 'is_featured', 'is_best_seller', 'is_active', 'component_type']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_featured', 'is_best_seller', 'is_active']
    inlines = [ProductImageInline, ReviewInline]
    fieldsets = [
        ('Basic Information', {'fields': ['category', 'name', 'slug', 'description', 'specifications']}),
        ('Pricing & Stock', {'fields': ['price', 'compare_price', 'stock', 'image']}),
        ('Classification', {'fields': ['is_featured', 'is_best_seller', 'is_custom_build', 'component_type', 'is_active']}),
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['product__name', 'user__username', 'comment']
