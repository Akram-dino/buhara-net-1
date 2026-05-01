from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded',
                'placeholder': 'Email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded',
                'placeholder': 'Last name'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'w-full border border-gray-300 px-4 py-3 rounded',
            'placeholder': 'Enter password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'w-full border border-gray-300 px-4 py-3 rounded',
            'placeholder': 'Confirm password'
        })


class AdminUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full border border-gray-300 px-4 py-3 rounded'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['is_active'].widget.attrs.update({
            'class': 'h-4 w-4'
        })