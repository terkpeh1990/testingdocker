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
from purchase_order.models import LocalPurchasingOrder
import os



@login_required(login_url='authentication:login')
@permission_required('inventory.custom_view_restock',raise_exception = True)
def restock(request):
    if request.user.is_superuser:
        restock_list = Restocks.objects.all()
        app_model = Companymodule.objects.all()
    else:
        product_list = Restocks.objects.filter(tenant_id=request.user.devision.tenant_id.id)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        restock_list = Restocks.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    template = 'inventory/restock/restock.html'
    context = {
        'restock_list': restock_list,
        'heading': 'Certification Status',
        'pageview': 'Restock',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_restock',raise_exception = True)
def add_restock(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = RestockForm(request.POST,request=request)
        if form.is_valid():
            restock = form.save(commit=False)

            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            restock.tenant_id = tenant_id
            restock.save()
            messages.info(request,'Restock Initiated, Please add or upload Products')
            return redirect('inventory:add-restock-details' , restock.id)
    else:
        form = RestockForm(request=request)

    template = 'inventory/restock/create-restock.html'
    context = {
        'form':form,
        'heading': 'New Restock',
        'pageview': 'List of Restock',
        'app_model':app_model
    }
    return render(request,template,context)




def add_restock_detail(request,restock_id):
    restock = Restocks.objects.get(id=restock_id)
    detail = Restock_details.objects.filter(restock_id=restock.id)
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        product = Products.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        product = Products.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = RestockDetailForm(request.POST)
        prod = request.POST.get("product")
        a,_ = prod.split('-----')
        print(a)
        print(prod)
        
        if form.is_valid():
            tenant =request.user.devision.tenant_id.id
            product =Products.objects.get(name=a,tenant_id=tenant)
            print(product)
            inven = Inventory.objects.get(product_id__name = a,tenant_id=tenant)
            quantity = form.cleaned_data['quantity']
            expiring_date = form.cleaned_data['expiring_date']
            Restock_details.objects.get_or_create(restock_id=restock,product_id=inven.product_id,quantity=quantity,expiring_date=expiring_date)
            messages.info(request,'Item added')
            return redirect('inventory:add-restock-details' , restock.id)
    else:
        form = RestockDetailForm()

    template = 'inventory/restock/create-restock-detail.html'
    context = {
        'form':form,
        'heading': 'New Restock',
        'pageview': 'List of Restock',
        'app_model':app_model,
        'detail':detail,
        'restock':restock,
        'product':product
    }
    return render(request,template,context)

def edit_restock_detail(request,restock_id):
    restocks = Restock_details.objects.get(id=restock_id)
    restock = Restocks.objects.get(id=restocks.restock_id.id)
    detail = Restock_details.objects.filter(restock_id=restock.id)
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        product = Products.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        product = Products.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = RestockDetailForm(request.POST,instance=restocks)
        prod = request.POST.get("product")
        if form.is_valid():
            tenant =request.user.devision.tenant_id.id
            inven = Inventory.objects.get(product_id__name = prod,tenant_id=tenant)
            product_id = product_id=inven.product_id
            quantity = form.cleaned_data['quantity']
            expiring_date = form.cleaned_data['expiring_date']
            restocks.product_id = product_id
            restocks.quantity = quantity
            restocks.expiring_date =expiring_date
            restocks.restock_id =restock
            restocks.save()
            messages.info(request,'Item Updated')
            return redirect('inventory:add-restock-details' , restock.id)
    else:
        form = RestockDetailForm(instance=restocks)

    template = 'inventory/restock/update-restock-detail.html'
    context = {
        'form':form,
        'heading': 'Update Restock',
        'pageview': 'List of Restock',
        'app_model':app_model,
        'detail':detail,
        'product':product,
        'restock':restock,
        'item':restocks
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
# @permission_required('inventory.custom_delete_product')
def delete_restock_item(request,restock_id):
    restock= Restock_details.objects.get(id=restock_id)
    restock.delete()
    messages.error(request,'Item Deleted')
    return redirect('inventory:add-restock-details', restock_id )

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_update_restock',raise_exception = True)
def edit_restock(request,restock_id):
    restock = Restocks.objects.get(id=restock_id)
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    if request.method == 'POST':
        form = RestockForm(request.POST,instance=restock,request=request)
        if form.is_valid():
            restock=form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            restock.tenant_id = tenant_id
            restock.save()
            messages.info(request,'Restock Updated')
            return redirect('inventory:add-restock-details',restock.id)
    else:
        form = RestockForm(instance=restock,request=request)

    template = 'inventory/restock/create-restock.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Restocks',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
# @permission_required('inventory.custom_delete_product')
def delete_restock(request,restock_id):
    restock = Restocks.objects.get(id=restock_id)
    restock.delete()
    messages.error(request,'Restock Deleted')
    return redirect('inventory:restock-list')
   

@login_required(login_url='authentication:login')
def restock_detail_upload(request,restock_id):
    restock = Restocks.objects.get(id=restock_id)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            uploaded_file_url = fs.url(filename) 
            file_path = os.path.join(fs.location, filename) 
            if os.path.exists(file_path):            
                empexceldata = pd.read_excel(filename)        
                dbframe = empexceldata
                try:
                    for i in dbframe.itertuples():
                        try:
                            tenant =request.user.devision.tenant_id.id
                            inven = Inventory.objects.get(product_id__name = i.Products.title().strip(),tenant_id=tenant)
                            product_id = product_id=inven.product_id
                            Restock_details.objects.get_or_create(restock_id=restock,product_id=product_id,quantity=i.Quantity,expiring_date=i.ExpiringDate)
                        except Inventory.DoesNotExist:
                            pass
                    messages.info(request,'Restock Data Uploaded')
                    return redirect('inventory:add-restock-details',restock.id)  
                except IOError:
                    messages.error(request,'Restock Data Upload Error')
                    return redirect('inventory:add-restock-details',restock.id)  
            else:
                messages.error(request, 'File not found.')
            return redirect('inventory:add-restock-details',restock.id) 
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

def cancel_restock(request,restock_id):
    restock = Restocks.objects.get(id=restock_id)
    restock.status="Cancelled"
    restock.save()
    messages.error(request,'Restock Cancelled')
    return redirect('inventory:add-restock-details',restock.id)

def reverse_restock(request,restock_id):
    restock = Restocks.objects.get(id=restock_id)
    restock.status="Pending"
    restock.save()
    messages.info(request,'Restock Transaction Reversed')
    return redirect('inventory:add-restock-details',restock.id)

def approve_restock(request,restock_id):
    restock = Restocks.objects.get(id=restock_id)
    detail = Restock_details.objects.filter(restock_id=restock.id)
    for i in detail:
        try:
            inventory = Inventory.objects.get(product_id = i.product_id.id,tenant_id=restock.tenant_id)
            inventory.avialable_quantity += i.quantity
            inventory.save()
            Inventory_Details.objects.get_or_create(inventory_id = inventory,quantity_intake=i.quantity,expiring_date=i.expiring_date,batch_number=i.batch_number)
        except Inventory.DoesNotExist:
            pass
    restock.status="Approved"
    restock.save()
    messages.info(request,'Restock Approved ')
    return redirect('inventory:add-restock-details',restock.id)