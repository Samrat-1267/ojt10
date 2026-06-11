from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'price', 'quantity', 'total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'total', 'status', 'item_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'email', 'shipping_name']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['subtotal', 'shipping_cost', 'discount', 'total']

    fieldsets = [
        ('Customer Information', {'fields': ['user', 'email', 'phone']}),
        ('Shipping Address', {'fields': ['shipping_name', 'shipping_address', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country']}),
        ('Order Details', {'fields': ['subtotal', 'shipping_cost', 'discount', 'total', 'status', 'notes']}),
    ]
