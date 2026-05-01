from django import forms
from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['image', 'notes', 'latitude', 'longitude', 'location']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'w-full border border-borderline bg-white px-4 py-3 text-sm min-h-[120px] focus:outline-none focus:border-primary',
                'rows': 5,
                'placeholder': 'Describe visible symptoms such as spots, yellowing, drying, curling, or unusual patterns.'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'location': forms.HiddenInput(),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise forms.ValidationError("Please upload an image.")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        file_name = image.name.lower()

        if not any(file_name.endswith(ext) for ext in valid_extensions):
            raise forms.ValidationError("Only JPG, JPEG, PNG, and WEBP images are allowed.")

        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size must not exceed 5MB.")

        return image