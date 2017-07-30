from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'email', 'phone', 'price', 'is_paid')
        widgets = {
            # 'designer_price':forms.NumberInput(attrs={'min':'0'}),
            # 'category': forms.ChoiceField(attrs={'class': 'input-xlarge'}),
            # 'name': forms.TextInput(attrs={'class': 'input-xlarge'}),
        }