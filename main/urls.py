from django.urls import path
from . import views

# name needs to be same as in views function redirect

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('myproducts', views.myproducts, name='myproducts'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('create-customer', views.create_customer, name='create_customer'),
    path('create-invoice/<int:customer_id>', views.create_invoice, name='create_invoice'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('view-invoice/<int:invoice_id>', views.view_invoice, name='view_invoice'),
    path('invoice-history', views.view_history, name='invoice_history'),
    path('customer-list/', views.view_customer, name='customer_list'),
    path('create-supplier', views.create_supplier, name='create_supplier'),
    path('supplier-list', views.view_suppliers, name='view_suppliers')
]