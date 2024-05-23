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
@permission_required('fixedassets.custom_create_mothodofacquisition')
def methodofacquisition(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    methodofacquisition_list = MothodofAcquisition.objects.all()
    template = 'fixedassets/methodofacquisition/methodofacquisition.html'
    context = {
        'methodofacquisition_list': methodofacquisition_list,
        'heading': 'List of Method Of Acquisition',
        'pageview': 'Method Of Acquisition',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_mothodofacquisition')
def add_methodofacquisition(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = MothodofAcquisitionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            MothodofAcquisition.objects.get_or_create(name=name.title())
            messages.info(request,'Method Of Acquisition Saved')
            return redirect('fixedassets:methodofacquisition-list')
    else:
        form = MothodofAcquisitionForm()

    template = 'fixedassets/methodofacquisition/create-methodofacquisition.html'
    context = {
        'form':form,
        'heading': 'New Method Of Acquisition',
        'pageview': 'List of Method Of Acquisitions',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_mothodofacquisition')
def edit_methodofacquisition(request,methodofacquisition_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    methodofacquisition=MothodofAcquisition.objects.get(id=methodofacquisition_id)
    if request.method == 'POST':
        form = MothodofAcquisitionForm(request.POST,instance=methodofacquisition)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Method Of Acquisition Updated')
            return redirect('fixedassets:methodofacquisition-list')
    else:
        form = MothodofAcquisitionForm(instance=methodofacquisition)

    template = 'fixedassets/methodofacquisition/create-methodofacquisition.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Method Of Acquisitions',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_mothodofacquisition')
def delete_methodofacquisition(request,methodofacquisition_id):
    methodofacquisition=MothodofAcquisition.objects.get(id=methodofacquisition_id)
    methodofacquisition.delete()
    messages.error(request,'Method Of Acquisition Deleted')
    return redirect('fixedassets:methodofacquisition-list')
   
@login_required(login_url='authentication:login')
def methodofacquisition_upload(request):
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
                DataUploadThread(dbframe,action='methodofacquisition').start()
                messages.success(request,'Method Of Acquisition Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('fixedassets:methodofacquisition-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
