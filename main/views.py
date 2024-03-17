from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
import subprocess
from django.forms import formset_factory
from django.contrib import messages
from django.db.models import Sum, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import itemgetter


# def autodeploy(request):
#     # Execute the shell script for autodeployment
#     try:
#         subprocess.run(["/var/www/deploy.sh"], check=True)
#         return JsonResponse({'message': 'Autodeploy script executed successfully.'})
#     except subprocess.CalledProcessError as e:
#         return JsonResponse({'error': f'Error executing autodeploy script: {e}'}, status=500)

@login_required(login_url='/login')
def home(request):
    return render(request, 'main/home.html')


@login_required(login_url='/login')
def view_products(request):
    cur_usr = request.user

    products = Product.objects.filter(created_by=cur_usr)

    return render(request, 'main/myproducts.html', {"products": products})


@login_required(login_url='/login')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect("/view_products")
    else:
        form = ProductForm(user=request.user)

    return render(request, 'main/create_post.html', {"form": form})


@login_required(login_url='/login')
def create_invoice(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    products = Product.objects.all()  # Retrieve all products from the database
    InvoiceItemFormSet = formset_factory(InvoiceItemForm, extra=1)

    if request.method == 'POST':
        formset = InvoiceItemFormSet(request.POST)
        if formset.is_valid():
            # Get cart items from the session
            cart = request.session.get('cart', {})

            if not cart:
                messages.error(request, 'Cannot create invoice. Your cart is empty.')
                return redirect('create_invoice', customer_id=customer_id)

            # Create the invoice
            invoice = Invoice.objects.create(seller=request.user, customer=customer)

            # Create invoice items from cart data and associate them with the invoice
            invoice_items = []
            for product_id, item in cart.items():
                product = get_object_or_404(Product, id=product_id)
                quantity = item['quantity']
                invoice_item = InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity
                )
                invoice_items.append(invoice_item)

            # Update total price for the invoice
            invoice.update_total_price()

            # Clear cart session
            request.session.pop('cart', None)

            # Redirect to view_invoice with the newly created invoice's ID
            return redirect('view_invoice', invoice_id=invoice.id)
    else:
        formset = InvoiceItemFormSet()

    request.session['customer_id'] = customer_id

    return render(request, 'main/create_invoice.html', {'customer': customer, 'formset': formset, 'cart': request.session.get('cart', {}), 'products': products})


@login_required(login_url='/login')
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id is not None:
            # print(f'Received product id: {product_id}')
            quantity = int(request.POST.get('form-0-quantity', 1))

            product = get_object_or_404(Product, id=product_id)

            cart = request.session.get('cart', {})
            if product_id in cart:
                cart[product_id]['quantity'] += quantity
                cart[product_id]['price'] += float(product.price)*quantity
            else:
                cart[product_id] = {'title': product.title, 'quantity': quantity, 'price': float(product.price)*quantity}

            request.session['cart'] = cart
        else:
            print(f'Product id is None')

    customer_id = request.session.get('customer_id')

    return redirect('create_invoice', customer_id=customer_id)


@login_required(login_url='/login')
def view_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    # Get invoice details
    invoice_number = invoice.id
    invoice_date = invoice.generated_on
    grand_total = invoice.total_price

    # Get customer details
    customer_name = invoice.customer.name
    customer_address = invoice.customer.address
    customer_phone = invoice.customer.phone
    customer_email = invoice.customer.email

    # Get invoice items
    invoice_items = invoice.invoiceitem_set.all()

    context = {
        'invoice_number': invoice_number,
        'invoice_date': invoice_date,
        'grand_total': grand_total,
        'customer_name': customer_name,
        'customer_address': customer_address,
        'customer_phone': customer_phone,
        'customer_email': customer_email,
        'invoice_items': invoice_items,
    }

    return render(request, 'main/invoice_format.html', context)


@login_required(login_url='/login')
def view_history(request):
    user_invoices = Invoice.objects.filter(seller=request.user).annotate(
        total_quantity=Sum('invoiceitem__quantity'),
        total_price_sum=Sum('invoiceitem__total_price'),
    ).order_by('-id')

    for invoice in user_invoices:
        # Fetch all product titles for this invoice
        product_titles = [item.product.title for item in invoice.invoiceitem_set.all()]
        # Concatenate the product titles
        invoice.item_names = ', '.join(product_titles)

    return render(request, 'main/invoice_history.html', {'user_invoices': user_invoices})


@login_required(login_url='/login')
def view_customer(request):
    cur_usr = request.user

    customers = Customer.objects.filter(created_by=cur_usr).only('id', 'created_at', 'img_url', 'name', 'phone', 'email', 'birth_date')
    return render(request, 'main/customer_list.html', {'customers': customers})


@login_required(login_url='/login')
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return redirect('view_customer')
    else:
        form = CustomerForm()

    return render(request, 'main/create_customer.html', {'form': form})


@login_required(login_url='/login')
def view_suppliers(request):
    cur_usr = request.user

    supplier = Supplier.objects.filter(created_by=cur_usr).only('id', 'created_at', 'img_url', 'name', 'phone', 'email', 'birth_date')
    return render(request, 'main/supplier_list.html', {'suppliers': supplier})


@login_required(login_url='/login')
def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.created_by = request.user
            supplier.save()
            return redirect('view_suppliers')
    else:
        form = SupplierForm()

    return render(request, 'main/create_supplier.html', {'form': form})


@csrf_protect
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




@login_required(login_url='/login')
def mystock(request):
    cur_user = request.user


    stocks = Product.objects.filter(created_by_id=cur_user).values('id', 'updated_at', 'supplier_id_id', 'title', 'stock_count', 'buying_price', 'is_cash').order_by('stock_count')

    paginator = Paginator(stocks, 10)  # Assuming 10 items per page, adjust as needed
    page_number = request.GET.get('page')  # Get the current page number from the query string

    try:
        page_stocks = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_stocks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_stocks = paginator.page(paginator.num_pages)
    



    stock_res = []
    c = 1
    for product in page_stocks:
        supplier_query_res = Supplier.objects.filter(id=product["supplier_id_id"]).values("name", "phone").first()
        supplier_name = supplier_query_res["name"] if supplier_query_res else ""
        supplier_phone = supplier_query_res["phone"] if supplier_query_res else ""

        is_cash  = "নগদ/বাকি"
        if product["is_cash"] == True:
            is_cash = "নগদ"
        else:
            is_cash = 'বাকি'

        new = {
            "sl": c,
            "updated_at": product["updated_at"],
            "supplier_name": supplier_name,
            "supplier_mobile": supplier_phone,
            "title": product["title"],
            "stock_count": product["stock_count"],
            "amount": product["stock_count"] * product["buying_price"],
            'is_cash': is_cash
        }
        stock_res.append(new)
        c+=1

   

    return render(request, 'main/mystock.html', {"pages": page_stocks, "stocks": stock_res})





@login_required(login_url='/login')
@require_http_methods(["DELETE"])
def delete_stock(request, stock_id):
    try:
        stock = Product.objects.get(id=stock_id, created_by=request.user)
        stock.delete()
        return JsonResponse({"message": "Stock item deleted successfully"}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Stock item not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@login_required(login_url='/login')
def update_stock(request, stock_id):
    if request.method == 'POST':
        # Retrieve the stock item from the database
        stock_item = get_object_or_404(Product, id=stock_id,created_by=request.user)
        
        # Update only the product_quantity field with the new value from the form
        new_product_quantity = request.POST.get('product_quantity')
        stock_item.stock_count = new_product_quantity
        
        # Save the updated stock item
        stock_item.save()

        # Optionally, you can update other fields here if needed
        
        # Return a JSON response indicating success
        return JsonResponse({'message': 'Stock item updated successfully'})

    # Handle other HTTP methods if needed
