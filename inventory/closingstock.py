# from msilib.schema import Error
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from authentication.forms import UploadFileForm
from django.contrib.auth.decorators import login_required, permission_required
from .upload_thread import *
import pandas as pd
from tablib import Dataset
from django.core.files.storage import FileSystemStorage
from appsystem.models import *
from django.views.generic.list import ListView
from django.utils import timezone


@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_product',raise_exception = True)
def closing_stock(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        closingstock_list = Closing_Stock.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        closingstock_list = Closing_Stock.objects.filter(tenant_id=request.user.devision.tenant_id.id)
    template = 'inventory/products/closing-stock.html'
    context = {
        'closingstock_list': closingstock_list,
        'heading': 'List of Closing Stock',
        'pageview': 'Closing Stock',
        'app_model':app_model
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_product',raise_exception = True)
def closingstock_product(request,closing_stock_id):
    closing_stock = Closing_Stock.objects.get(id=closing_stock_id)
    if request.user.is_superuser:
        product_list = Closing_Stock_Inventory.objects.filter(closing_id =closing_stock.id)
        app_model = Companymodule.objects.all()
    else:
        product_list = product_list = Closing_Stock_Inventory.objects.filter(closing_id =closing_stock.id)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    template = 'inventory/products/closing_stock_inventory.html'
    context = {
        'product_list': product_list,
        'heading': 'List of Products',
        'pageview': 'Products',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_view_product',raise_exception = True)
def closingstock_detail_product(request,closing_stock_product_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    inventory = Closing_Stock_Inventory.objects.get(id=closing_stock_product_id)
    product=Products.objects.get(id=inventory.product_id.id)
    inventory_detail = Closing_Stock_Inventory_Details.objects.filter(closing_inventory_id=inventory.id)
    assets=Assets.objects.filter(product_id=inventory.product_id.id, tenant_id = inventory.closing_id.tenant_id.id)
    for i in assets:
        print(i.serial_number)
    # print(user_permission)
    template = 'inventory/products/closing_stock_inventory_detail.html'
    context = {
        'inventory':inventory,
        'inventory_detail':inventory_detail,
        'heading': 'Product Detail',
        'pageview': 'Details',
        'app_model':app_model,
        'assets':assets
    }
    return render(request,template,context)



def close_stock(request):
   
    clsoing_stock = Closing_Stock.objects.create(tenant_id=request.user.devision.tenant_id)
    inventory = Inventory.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    for item in inventory:
        cc=Inventory_Details.objects.filter(inventory_id=item.id)
        itemstock = Closing_Stock_Inventory.objects.create(closing_id=clsoing_stock,product_id=item.product_id,avialable_quantity=item.avialable_quantity,tenant_id = clsoing_stock.tenant_id)
        for i in cc:
            stc = Closing_Stock_Inventory_Details.objects.create(closing_inventory_id=itemstock,quantity_intake=i.quantity_intake,quantity_requested=i.quantity_requested,avialable_quantity=i.avialable_quantity,batch_number=i.batch_number,date_received=i.date_received,expiring_date=i.expiring_date)
    return redirect('inventory:closing-stock-products',clsoing_stock.id )    
