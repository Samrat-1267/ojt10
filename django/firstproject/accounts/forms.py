from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Address, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'full_name', 'phone', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-input'}),
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-input'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'state': forms.TextInput(attrs={'class': 'form-input'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input'}),
            'country': forms.TextInput(attrs={'class': 'form-input'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
