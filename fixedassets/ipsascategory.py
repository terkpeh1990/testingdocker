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
@permission_required('fixedassets.custom_create_IPSAS_category')
def ipsascategory(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    ipsascategory_list = IPSASCategory.objects.all()
    template = 'fixedassets/ipsascategory/ipsascategory.html'
    context = {
        'ipsascategory_list': ipsascategory_list,
        'heading': 'List of IPSAS Categories',
        'pageview': 'IPSAS Category',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_IPSAS_category')
def add_ipsascategory(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = IPSASCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            classification = form.cleaned_data['classification']
            IPSASCategory.objects.get_or_create(name=name.title(),classification=classification)
            messages.info(request,'IPSAS Category Saved')
            return redirect('fixedassets:ipsascategory-list')
    else:
        form = IPSASCategoryForm()

    template = 'fixedassets/ipsascategory/create-ipsascategory.html'
    context = {
        'form':form,
        'heading': 'New IPSAS Category',
        'pageview': 'List of IPSAS Categories',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_IPSAS_category')
def edit_ipsascategory(request,ipsascategory_id):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    ipsascategory=IPSASCategory.objects.get(id=ipsascategory_id)
    if request.method == 'POST':
        form = IPSASCategoryForm(request.POST,instance=ipsascategory)
        if form.is_valid():
            form.save()
            
            messages.info(request,'IPSAS Category Updated')
            return redirect('fixedassets:ipsascategory-list')
    else:
        form = IPSASCategoryForm(instance=ipsascategory)

    template = 'fixedassets/ipsascategory/create-ipsascategory.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of IPSAS Categories',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_IPSAS_category')
def delete_ipsascategory(request,ipsascategory_id):
    ipsascategory=IPSASCategory.objects.get(id=ipsascategory_id)
    ipsascategory.delete()
    messages.error(request,'IPSAS Category Deleted')
    return redirect('fixedassets:ipsascategory-list')
   
@login_required(login_url='authentication:login')
def ipsascategory_upload(request):
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
                DataUploadThread(dbframe,action='ipsascategory').start()
                messages.success(request,'IPSAS Category Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('fixedassets:ipsascategory-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
