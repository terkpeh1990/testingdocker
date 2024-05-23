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
@permission_required('fixedassets.custom_create_gfscategory')
def gfscategory(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    gfscategory_list = GFSCategory.objects.all()
    template = 'fixedassets/gfscategory/gfscategory.html'
    context = {
        'gfscategory_list': gfscategory_list,
        'heading': 'List of GFS Category',
        'pageview': 'GFS Category',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_gfscategory')
def add_gfscategory(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = GFSCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            gfscategory = GFSCategory.objects.get_or_create(name=name.title(),code=code)
            messages.info(request,'GFS Category Saved')
            return redirect('fixedassets:gfscategory-list')
    else:
        form = GFSCategoryForm()

    template = 'fixedassets/gfscategory/create-gfscategory.html'
    context = {
        'form':form,
        'heading': 'New GFS Category',
        'pageview': 'List of GFS Category',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_gfscategory')
def edit_gfscategory(request,gfscategory_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    gfscategory=GFSCategory.objects.get(id=gfscategory_id)
    if request.method == 'POST':
        form = GFSCategoryForm(request.POST,instance=gfscategory)
        if form.is_valid():
            form.save()
            
            messages.info(request,'GFS Category Updated')
            return redirect('fixedassets:gfscategory-list')
    else:
        form = GFSCategoryForm(instance=gfscategory)

    template = 'fixedassets/gfscategory/create-gfscategory.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of GFS Category',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_gfscategory')
def delete_gfscategory(request,gfscategory_id):
    gfscategory=GFSCategory.objects.get(id=gfscategory_id)
    gfscategory.delete()
    messages.error(request,'GFS Category Deleted')
    return redirect('fixedassets:gfscategory-list')
   
@login_required(login_url='authentication:login')
def gfscategory_upload(request):
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
                DataUploadThread(dbframe,action='gfscategory').start()
                messages.success(request,'GFS Category Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('fixedassets:gfscategory-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
