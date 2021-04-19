from django import forms

from .models import Product, ProductImage

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', ]

ImageFormSet = forms.modelformset_factory(
    ProductImage,
    form=ImageForm,
    extra=3,
    max_num=5,
    can_delete=True
)

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

# <a href="{% url 'edit-product' product.id %}">