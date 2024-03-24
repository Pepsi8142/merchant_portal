from django.urls import path
from . import views

# name needs to be same as in views function redirect

urlpatterns = [
    path('sign-up', views.sign_up, name='sign_up'),
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('view_products', views.view_products, name='view_products'),
    path('create_product', views.create_product, name='create_product'),
    path('create-customer', views.create_customer, name='create_customer'),
    path('create-invoice', views.create_invoice, name='create_invoice'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('view_invoice/<int:invoice_id>', views.view_invoice, name='view_invoice'),
    path('invoice-history', views.view_history, name='invoice_history'),
    path('customer-list', views.view_customer, name='view_customer'),
    path('create-supplier', views.create_supplier, name='create_supplier'),
    path('supplier-list', views.view_suppliers, name='view_suppliers'),
    path('mystock',views.mystock, name = 'mystock'),
    path('delete_stock/<int:stock_id>', views.delete_stock, name='delete_stock'),
    path('update_stock/<int:stock_id>/', views.update_stock, name='update_stock'),
]