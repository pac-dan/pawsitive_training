from django import forms
from .models import Training, TrainingCategory


class TrainingForm(forms.ModelForm):
    """
    Form for staff to create and edit training videos.
    """
    class Meta:
        model = Training
        fields = ['title', 'description', 'category', 'video_file', 
                  'thumbnail', 'is_free', 'order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter training video title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter description of the training video'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_free': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }
        labels = {
            'title': 'Video Title',
            'description': 'Description',
            'category': 'Category',
            'video_file': 'Video File',
            'thumbnail': 'Thumbnail Image',
            'is_free': 'Free to view (no subscription required)',
            'order': 'Display Order',
        }
        help_texts = {
            'order': 'Lower numbers appear first (0 = first)',
            'is_free': 'Check this to make the video available to all users',
            'video_file': 'Upload an MP4 video file',
            'thumbnail': 'Upload a preview image for the video',
        }
    
    def clean_order(self):
        """Ensure order is not negative."""
        order = self.cleaned_data.get('order')
        if order and order < 0:
            raise forms.ValidationError('Order cannot be negative.')
        return order

