from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'final_disease_name',
            'final_recommendation',
            'expert_notes',
            'review_status',
        ]
        widgets = {
            'final_disease_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter final disease name'
            }),
            'final_recommendation': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded focus:outline-none focus:ring-2 focus:ring-primary',
                'rows': 4,
                'placeholder': 'Enter final recommendation'
            }),
            'expert_notes': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded focus:outline-none focus:ring-2 focus:ring-primary',
                'rows': 3,
                'placeholder': 'Optional expert notes'
            }),
            'review_status': forms.Select(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded focus:outline-none focus:ring-2 focus:ring-primary'
            }),
        }