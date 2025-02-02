from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms.widgets import DateInput


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
    PAYMENT_CHOICES = [
        (True, 'নগদ'),
        (False, 'বাকি')
    ]

    cash_payment = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        label='পেমেন্ট'
    )

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
            'supplier_id': 'সাপ্লায়ার'
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        is_cash = self.cleaned_data['cash_payment']
        product.is_cash = is_cash
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
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'})
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
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img_url'].required = False


class CustomerSelectionForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.none(), empty_label="কাস্টমার নির্বাচন করুন")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CustomerSelectionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['customer'].queryset = Customer.objects.filter(created_by=user)