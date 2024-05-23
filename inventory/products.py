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
import os
from fixedassets.models import *



@login_required(login_url='authentication:login')
@permission_required('inventory.custom_view_product',raise_exception = True)
def product(request):
    if request.user.is_superuser:
        product_list = Inventory.objects.all()
        app_model = Companymodule.objects.all()
    else:
        product_list = Inventory.objects.filter(tenant_id=request.user.devision.tenant_id.id)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    template = 'inventory/products/product.html'
    context = {
        'product_list': product_list,
        'heading': 'List of Products',
        'pageview': 'Products',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_product',raise_exception = True)
def add_product(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = ProductForm(request.POST,request=request)
        if form.is_valid():
            product = form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            product.tenant_id = tenant_id
            product.save()
            print(product.name, product.tenant_id)
            try:
                inventory = Inventory.objects.get(product_id=product,avialable_quantity=0,tenant_id = tenant_id)
            except Inventory.DoesNotExist:
                inventory = Inventory.objects.create(product_id=product,avialable_quantity=0,tenant_id = tenant_id)
            detail = Inventory_Details.objects.get_or_create(inventory_id = inventory,quantity_intake=0,batch_number=0)
            messages.info(request,'Product Saved')
            return redirect('inventory:view-product' , product.id)
    else:
        form = ProductForm(request=request)

    template = 'inventory/products/create-product.html'
    context = {
        'form':form,
        'heading': 'New Product',
        'pageview': 'List of Products',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_update_product',raise_exception = True)
def edit_product(request,product_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    product=Products.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product,request=request)
        if form.is_valid():
            product=form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            product.tenant_id = tenant_id
            product.save()
            messages.info(request,'Product Updated')
            return redirect('inventory:view-product',product.id)
    else:
        form = ProductForm(instance=product,request=request)

    template = 'inventory/products/create-product.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Products',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
# @permission_required('inventory.custom_delete_product')
def delete_product(request,product_id):
    product=Products.objects.get(id=product_id)
    product.delete()
    messages.error(request,'Product Deleted')
    return redirect('inventory:product-list')
   
@login_required(login_url='authentication:login')
def product_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            uploaded_file_url = fs.url(filename)
            # Get the complete path to the uploaded file
            file_path = os.path.join(fs.location, filename)
            if os.path.exists(file_path):  # Check if the file exists
                empexceldata = pd.read_excel(file_path)
                dbframe = empexceldata
                ProductThread(dbframe).start()
                messages.success(request,'Productt Data Upload Started')
            
            else:
                messages.error(request, 'File not found.')
            return redirect('inventory:product-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required(login_url='authentication:login')
@permission_required('inventory.custom_view_product',raise_exception = True)
def detail_product(request,product_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    inventory = Inventory.objects.get(id=product_id)
    product=Products.objects.get(id=inventory.product_id.id)
    inventory_detail = Inventory_Details.objects.filter(inventory_id=inventory.id)
    assets=FixedAsset.objects.filter(product=inventory.product_id.id)
    for i in assets:
        print(i.asset_id)
    # print(user_permission)
    template = 'inventory/products/product-detail-view.html'
    context = {
        'inventory':inventory,
        'inventory_detail':inventory_detail,
        'heading': 'Product Detail',
        'pageview': 'Details',
        'app_model':app_model,
        'assets':assets
    }
    return render(request,template,context)

login_required(login_url='authentication:login')
# @permission_required(['inventory.custom_approve_capital_requisition','inventory.custom_approve_consumable_requisition'],raise_exception = True)
def aviable_assets(request):
    if request.user.is_superuser:
        assets_list = Assets.objects.filter(status=False)
        app_model = Companymodule.objects.all()
    else:
        if request.user.has_perm('inventory.authentication.custom_view_user'):
            assets_list = Assets.objects.filter(product_id__category_id.name == "IT Equipments",tenant_id=request.user.devision.tenant_id.id,status=False)
        else:
            assets_list = Assets.objects.filter(tenant_id=request.user.devision.tenant_id.id,status=False)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    template = 'inventory/products/available-assets.html'
    context = {
        'assets_list':assets_list
        }
    return render(request, template, context)
   
# class detail_product(ListView):
#     template_name = 'inventory/products/product-detail-view.html'
#     context_object_name = 'inventory'
#     paginated_by = 10

#     def get_queryset(self, **kwargs):
#         inventory_id = self.kwargs['product_id']
#         queryset = {'inventory': Inventory.objects.get(id=inventory_id), 
#                    'inventory_detail': Inventory_Details.objects.filter(inventory_id=inventory_id),
#                    'assets':Assets.objects.filter(product_id=inventory.product_id.id, tenant_id = inventory.tenant_id.id)
#                    }
#         return queryset
