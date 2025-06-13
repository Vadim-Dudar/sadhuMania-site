from django import forms
from content.models import CarouselImage

class CarouselImageForm(forms.ModelForm):
    class Meta:
        model = CarouselImage
        fields = ['button', 'title', 'image', 'slide_type', 'order']
