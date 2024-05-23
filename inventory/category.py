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
@permission_required('inventory.custom_view_category',raise_exception = True)
def category(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        category_list = Categorys.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        category_list = Categorys.objects.filter(tenant_id=request.user.devision.tenant_id.id)
       
   
    template = 'inventory/products/category.html'
    context = {
        'category_list': category_list,
        'heading': 'List of Categories',
        'pageview': 'Categories',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_category',raise_exception = True)
def add_category(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = CategoryForm(request.POST,request=request)
        if form.is_valid():
            name = form.cleaned_data['name']
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            category = Categorys.objects.get_or_create(name=name.title(),tenant_id=tenant_id)
            messages.info(request,'Category Saved')
            return redirect('inventory:category-list')
    else:
        form = CategoryForm(request=request)

    template = 'inventory/products/create-category.html'
    context = {
        'form':form,
        'heading': 'New Category',
        'pageview': 'List of Categories',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_update_category',raise_exception = True)
def edit_category(request,category_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    category=Categorys.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category,request=request)
        if form.is_valid():
            category = form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            category.tenant_id = tenant_id
            category.save()
            messages.info(request,'Category Updated')
            return redirect('inventory:category-list')
    else:
        form = CategoryForm(instance=category,request=request)

    template = 'inventory/products/create-category.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Categories',
        'app_model':app_model
        
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_delete_category',raise_exception = True)
def delete_category(request,category_id):
    category=Categorys.objects.get(id=category_id)
    category.delete()
    messages.error(request,'Category Deleted')
    return redirect('inventory:category-list')
   
@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_category',raise_exception = True)
def category_upload(request):
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
                CategoryThread(dbframe).start()
                messages.success(request,'Category Data Uploaded Successfully')
            
            else:
                messages.error(request, 'File not found.')
            return redirect('inventory:category-list')
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
