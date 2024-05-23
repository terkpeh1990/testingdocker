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
import os





@login_required(login_url='authentication:login')
@permission_required('inventory.custom_view_brand')
def brand(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        brand_list = Brands.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        brand_list = Brands.objects.filter(tenant_id=request.user.devision.tenant_id.id)
    template = 'inventory/products/brands.html'
    context = {
        'brand_list': brand_list,
        'heading': 'List of Brands',
        'pageview': 'Brands',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_brand')
def add_brand(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = BrandForm(request.POST,request=request)
        if form.is_valid():
            name = form.cleaned_data['name']
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            category = Brands.objects.get_or_create(name=name.title(),tenant_id=tenant_id)
            messages.info(request,'Brand Saved')
            return redirect('inventory:brand-list')
    else:
        form = BrandForm(request=request)

    template = 'inventory/products/create-brand.html'
    context = {
        'form':form,
        'heading': 'New Brand',
        'pageview': 'List of Brands',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_update_brand')
def edit_brand(request,brand_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    brand=Brands.objects.get(id=brand_id)
    if request.method == 'POST':
        form = BrandForm(request.POST,instance=brand,request=request)
        if form.is_valid():
            brand = form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            brand.tenant_id = tenant_id
            brand.save()
            messages.info(request,'Brand Updated')
            return redirect('inventory:brand-list')
    else:
        form = BrandForm(instance=brand,request=request)

    template = 'inventory/products/create-brand.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Brands',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_delete_brand')
def delete_brand(request,brand_id):
    brand=Brands.objects.get(id=brand_id)
    brand.delete()
    messages.error(request,'Brand Deleted')
    return redirect('inventory:brand-list')
   
@login_required(login_url='authentication:login')
def brand_upload(request):
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
                BrandThread(dbframe).start()
                messages.success(request,'Brand Data Uploaded Successfully')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('inventory:brand-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
