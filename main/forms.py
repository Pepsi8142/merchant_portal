from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Customer, Invoice


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "img_url"]


class InvoiceForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=50)
    customer_address = forms.CharField(max_length=150)
    customer_phone = forms.CharField(max_length=13)
    customer_email = forms.EmailField(required=False)
    quantity = forms.IntegerField(min_value=0) # ensure only positive input

    class Meta:
        model = Invoice
        fields = ['customer_name', 'customer_address', 'customer_phone', 'customer_email', 'quantity']

    def save(self, product_id=None, seller=None, commit=True):
        customer_name = self.cleaned_data.get('customer_name')
        customer_address = self.cleaned_data.get('customer_address')
        customer_phone = self.cleaned_data.get('customer_phone')
        customer_email = self.cleaned_data.get('customer_email')
        quantity = self.cleaned_data.get('quantity')

        customer_email = customer_email if customer_email else None

        customer = Customer.objects.create(
            name=customer_name,
            address=customer_address,
            phone=customer_phone,
            email=customer_email
        )

        product = Product.objects.get(pk=product_id)  # Query the Product model to get the product
        total_price = product.price * quantity  # Calculate the total price

        invoice = Invoice(
            seller=seller,
            customer=customer,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        if commit:
            customer.save()
            invoice.save()

        return invoice


