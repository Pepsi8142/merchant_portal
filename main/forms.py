from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # shop_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["username", 'email', "password1", "password2"]
        labels = {
            'username': 'নাম',
            'email': 'ইমেইল'
        }


class ProductForm(forms.ModelForm):
    cash_payment = forms.BooleanField(required=False, label='নগদ')
    credit_payment = forms.BooleanField(required=False, label='বাকি')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['supplier_id'].queryset = user.supplier_set.all()

    class Meta:
        model = Product
        fields = ["title", "description", "buying_price", "selling_price", "img_url", "stock_count", "supplier_id"]
        labels = {
            'title': 'পণ্যের নাম',
            'description': 'পণ্যের বিবরণ',
            'buying_price': 'ক্রয়মূল্য',
            'selling_price': 'বিক্রয়মূল্য',
            'img_url': 'ছবি',
            'stock_count': 'স্টকের সংখ্যা',
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        is_cash = self.cleaned_data.get('cash_payment', False)
        is_credit = self.cleaned_data.get('credit_payment', False)
        # Set is_cash based on tickbox values
        if is_cash and not is_credit:
            product.is_cash = True
        elif not is_cash and is_credit:
            product.is_cash = False
        else:
            # If neither tickbox is checked, assume credit payment
            product.is_cash = False
        if commit:
            product.save()
        return product


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'birth_date', 'img_url']
        labels = {
            'name': 'কাস্টমারের নাম',
            'phone': 'মোবাইল নম্বর',
            'email': 'ইমেইল',
            'birth_date': 'জন্ম তারিখ',
            'img_url': 'ছবি'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img_url'].required = False


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'email', 'birth_date', 'img_url']
        labels = {
            'name': 'সাপ্লাইয়ারের নাম',
            'phone': 'মোবাইল নম্বর',
            'email': 'ইমেইল',
            'birth_date': 'জন্ম তারিখ',
            'img_url': 'ছবি'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img_url'].required = False


class InvoiceItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="--- Please select a product ---")
    quantity = forms.IntegerField(min_value=1, initial=1)