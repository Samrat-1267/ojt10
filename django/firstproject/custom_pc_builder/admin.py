from django.contrib import admin
from .models import CompatibilityRule, SavedBuild


@admin.register(CompatibilityRule)
class CompatibilityRuleAdmin(admin.ModelAdmin):
    list_display = ['component_type', 'compatible_with_type', 'notes']
    list_filter = ['component_type']
    search_fields = ['component_type', 'compatible_with_type']


@admin.register(SavedBuild)
class SavedBuildAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total_price', 'is_compatible', 'created_at']
    list_filter = ['is_compatible', 'created_at']
    search_fields = ['name', 'user__username']
