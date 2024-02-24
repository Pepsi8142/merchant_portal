from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('create-customer', views.create_customer, name='create_customer'),
    path('create-invoice/<int:customer_id>', views.create_invoice, name='create_invoice'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('view-invoice/<int:invoice_id>', views.view_invoice, name='view_invoice'),
    path('invoice-history/', views.view_history, name='invoice_history'),
]