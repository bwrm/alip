from django import forms
from .models import Product, DetailProduce
from django.core.validators import MinValueValidator


class ProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'designer_price', 'description',)
        widgets = {
            # 'designer_price':forms.NumberInput(attrs={'min':'0'}),
            # 'category': forms.ChoiceField(attrs={'class': 'input-xlarge'}),
            # 'name': forms.TextInput(attrs={'class': 'input-xlarge'}),
        }

class ProductProduceForm(forms.ModelForm):
    class Meta:
        model = DetailProduce
        fields = ('price', 'days', 'shipping')