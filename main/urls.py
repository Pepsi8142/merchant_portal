from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('create-invoice/<int:product_id>', views.create_invoice, name='create_invoice'),
    path('view-invoice/<int:invoice_id>', views.view_invoice, name='view_invoice'),
    path('invoice-history/', views.view_history, name='invoice_history'),
]