from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('__all__')
        exclude = ('author','item','is_published','average_rating')
        widgets = {
            'rating': forms.NumberInput(attrs={'min':'1','max':'5'}),
            # 'name': forms.TextInput(attrs={'class': 'input-xlarge'}),
        }
