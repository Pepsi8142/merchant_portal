from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    img_url = models.ImageField(upload_to='products/', default=None, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13, unique=True) # only mandatory
    email = models.EmailField(blank=True, null=True)  # Optional email field
    birth_date = models.DateField(blank=True, null=True)
    img_url = models.ImageField(upload_to='customers/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"


class Supplier(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13, unique=True) # only mandatory
    email = models.EmailField(blank=True, null=True)  # Optional email field
    birth_date = models.DateField(blank=True, null=True)
    img_url = models.ImageField(upload_to='suppliers/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"


class Invoice(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total_price(self):
        total_price = self.invoiceitem_set.aggregate(total=models.Sum('total_price'))['total']
        self.total_price = total_price if total_price is not None else 0
        self.save()

    def __str__(self):
        return f"Invoice for {self.customer.name} - {self.generated_on} - {self.total_price}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Calculate total price based on product price and quantity
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} - {self.product.title} - {self.total_price}"