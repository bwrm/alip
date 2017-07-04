from django import forms

from .models import Photo, Files


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )

class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file', )

