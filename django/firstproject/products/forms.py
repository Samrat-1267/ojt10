from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-input', 'placeholder': 'Share your experience...'}),
        }
