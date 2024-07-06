from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
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


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    img_url = models.ImageField(upload_to='products/', null=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    stock_count = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True)
    is_cash = models.BooleanField(default=False, null=False)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


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
        self.total_price = self.product.selling_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} - {self.product.title} - {self.total_price}"


class Expenditure(models.Model):
    expense_id = models.PositiveIntegerField(primary_key=True, auto_created=True, unique=True)
    expense_type = models.CharField(max_length=20)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expense_date = models.DateField(auto_now_add=True)
    voucher_no = models.CharField(max_length=20)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(max_length=50)

    def save(self, *args, **kwargs):
        self.total_expense = self.expense_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Total Expense is {self.total_expense} taka upto {self.expense_date}"
