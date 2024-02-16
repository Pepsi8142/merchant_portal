from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProductForm, InvoiceForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product, Invoice
from django.http import HttpResponse
from django.http import JsonResponse
import subprocess

def autodeploy(request):
    # Execute the shell script for autodeployment
    try:
        subprocess.run(["/var/www/deploy.sh"], check=True)
        return JsonResponse({'message': 'Autodeploy script executed successfully.'})
    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': f'Error executing autodeploy script: {e}'}, status=500)


@login_required(login_url='/login')
def home(request):
    posts = Product.objects.all()

    return render(request, 'main/home.html', {"posts": posts})


@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = ProductForm()

    return render(request, 'main/create_post.html', {"form": form})


@login_required(login_url='/login')
def create_invoice(request, product_id):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(product_id=product_id, seller=request.user)
            return redirect('view_invoice', invoice_id=invoice.id)
    else:
        form = InvoiceForm()

    return render(request, 'main/create_invoice.html', {'form': form})


@login_required(login_url='/login')
def view_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    customer_name = invoice.customer.name
    customer_address = invoice.customer.address
    customer_phone = invoice.customer.phone
    customer_email = invoice.customer.email
    product_name = invoice.product.title
    quantity = invoice.quantity
    amount = invoice.total_price

    context = {
        'invoice': invoice,
        'customer_name': customer_name,
        'customer_address': customer_address,
        'customer_phone': customer_phone,
        'customer_email': customer_email,
        'product_name': product_name,
        'quantity': quantity,
        'amount': amount
    }

    return render(request, 'main/invoice_format.html', context)


@login_required(login_url='/login')
def view_history(request):
    user_invoices = Invoice.objects.filter(seller=request.user).order_by('-id')
    return render(request, 'main/invoice_history.html', {'user_invoices': user_invoices})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
