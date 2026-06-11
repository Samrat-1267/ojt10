from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'total']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'item_count', 'subtotal', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_id']
    inlines = [CartItemInline]
