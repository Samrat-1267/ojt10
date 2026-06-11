from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'phone', 'shipping_name', 'shipping_address', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country', 'notes']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000'}),
            'shipping_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John Doe'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123 Main St'}),
            'shipping_address2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apt 4B'}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'shipping_state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '12345'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'United States'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Order notes (optional)'}),
        }
