from django import forms
from .models import TypeServices, Producer, MyUser


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['email', 'password']

class CutomProducerForm(forms.ModelForm):

    class Meta:
        model = Producer
        fields = (
            'public_name', 'is_cncmill', 'is_3d', 'is_cnclaser', 'street_number', 'route', 'locality', 'administrative_area_level_1',
                    'administrative_area_level_2', 'postal_code', 'country', 'latitude', 'longitude', 'postal_delivery',
                    'pickup_delivery', 'canprintinvoce', 'delivery_time',
        )
        widgets = {
            'street_number':forms.TextInput(attrs={'id': 'street_number', 'class': 'field'}),
            'route':forms.TextInput(attrs={'id': 'route', 'class': 'field'}),
            'locality':forms.TextInput(attrs={'id': 'locality', 'class': 'field'}),
            'administrative_area_level_1':forms.TextInput(attrs={'id': 'administrative_area_level_1', 'class': 'field'}),
            'administrative_area_level_2':forms.TextInput(attrs={'id': 'administrative_area_level_2', 'class': 'field'}),
            'postal_code':forms.TextInput(attrs={'id': 'postal_code', 'class': 'field'}),
            'country':forms.TextInput(attrs={'id': 'country', 'class': 'field'}),
            'latitude': forms.HiddenInput(attrs={'id': 'latitude', 'class': 'field'}),
            'longitude': forms.HiddenInput(attrs={'id': 'longitude', 'class': 'field'})
        }
        labels = {
            'latitude':'',
            'longitude':'',
        }

class TypeServiceForm(forms.ModelForm):
    class Meta:
        model = TypeServices
        fields = ['services']

    SERVICE_CHOICE = (
        ('0','3D Printing'),
        ('1','CNC Machining'),
        ('2','Laser Cutting / Engraving'),
    )
    services = forms.TypedChoiceField(choices=SERVICE_CHOICE, widget=forms.RadioSelect)

class PlainUserAccountForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'phone_number', 'company', 'locality', 'location', 'postal_code', 'country']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'last_name': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'phone_number': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'company': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'location': forms.TextInput(attrs={'class': 'input-xlarge'}),
        }

