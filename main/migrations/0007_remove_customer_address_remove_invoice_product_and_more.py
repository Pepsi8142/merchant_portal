# Generated by Django 5.0.2 on 2024-03-12 18:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_bought_on_invoice_generated_on'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='customer',
        #     name='address',
        # ),
        # migrations.RemoveField(
        #     model_name='invoice',
        #     name='product',
        # ),
        # migrations.RemoveField(
        #     model_name='invoice',
        #     name='quantity',
        # ),
        # migrations.AddField(
        #     model_name='customer',
        #     name='birth_date',
        #     field=models.DateField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='customer',
        #     name='created_by',
        #     field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        # ),
        # migrations.AddField(
        #     model_name='customer',
        #     name='img_url',
        #     field=models.ImageField(null=True, upload_to='customers/'),
        # ),
        # migrations.AddField(
        #     model_name='invoice',
        #     name='seller',
        #     field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        # ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        # migrations.AlterField(
        #     model_name='product',
        #     name='buying_price',
        #     field=models.DecimalField(null=True, decimal_places=2, max_digits=10),
        # ),
        # migrations.CreateModel(
        #     name='InvoiceItem',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('quantity', models.PositiveIntegerField()),
        #         ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
        #         ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.invoice')),
        #         ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
        #     ],
        # ),
        # migrations.CreateModel(
        #     name='Supplier',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('name', models.CharField(max_length=50)),
        #         ('phone', models.CharField(max_length=13, unique=True)),
        #         ('email', models.EmailField(blank=True, max_length=254, null=True)),
        #         ('birth_date', models.DateField(blank=True, null=True)),
        #         ('img_url', models.ImageField(null=True, upload_to='suppliers/')),
        #         ('created_at', models.DateTimeField(auto_now_add=True)),
        #         ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        #     ],
        # ),
    ]
