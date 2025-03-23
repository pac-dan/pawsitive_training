from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    """
    Form to handle user profile updates.
    """
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'image']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
