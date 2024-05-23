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
@permission_required('fixedassets.custom_create_subcategory')
def subcategory(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    subcategory_list = SubCategory.objects.all()
    template = 'fixedassets/subcategory/subcategory.html'
    context = {
        'subcategory_list': subcategory_list,
        'heading': 'List of Sub Categories',
        'pageview': 'Sub categotory',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_subcategory')
def add_subcategory(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ipsascategory = form.cleaned_data['ipsascategory']
            SubCategory.objects.get_or_create(name=name.title(),ipsascategory=ipsascategory)
            messages.info(request,'Sub Category Saved')
            return redirect('fixedassets:subcategory-list')
    else:
        form = SubCategoryForm()

    template = 'fixedassets/subcategory/create-subcategory.html'
    context = {
        'form':form,
        'heading': 'New Sub Category',
        'pageview': 'List of Sub Categories',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_subcategory')
def edit_subcategory(request,subcategory_id):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    subcategory=SubCategory.objects.get(id=subcategory_id)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST,instance=subcategory)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Sub Category Updated')
            return redirect('fixedassets:subcategory-list')
    else:
        form = SubCategoryForm(instance=subcategory)

    template = 'fixedassets/subcategory/create-subcategory.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Sub Categories',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_subcategory')
def delete_subcategory(request,subcategory_id):
    subcategory=SubCategory.objects.get(id=subcategory_id)
    subcategory.delete()
    messages.error(request,'Sub Category Deleted')
    return redirect('fixedassets:subcategory-list')
   
@login_required(login_url='authentication:login')
def subcategory_upload(request):
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
                DataUploadThread(dbframe,action='subcategory').start()
                messages.success(request,'Sub Category Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('fixedassets:subcategory-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
