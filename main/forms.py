from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    shop_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "img_url"]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'birth_date', 'img_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img_url'].required = False


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'email', 'birth_date', 'img_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img_url'].required = False


class InvoiceItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="--- Please select a product ---")
    quantity = forms.IntegerField(min_value=1, initial=1)