from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'cover_photo',
            'detail_photo_1',
            'detail_photo_2',
            'detail_photo_3',
            'plant_name',
            'previous_price',
            'current_price',
            'stock_count',
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Enter description...'}),
            'cover_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': True}),
            'detail_photo_1': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': True}),
            'detail_photo_2': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': True}),
            'detail_photo_3': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': True}),
            'plant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter plant name...', 'required': True}),
            'previous_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter previous price...', 'required': True}),
            'current_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter current price...', 'required': True}),
            'stock_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock count...', 'required': True}),
        }
