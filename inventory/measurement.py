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
@permission_required('inventory.custom_view_measuremnt',raise_exception = True)
def measurement(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        measurement_list = Unit_of_Measurement.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        measurement_list = Unit_of_Measurement.objects.filter(tenant_id=request.user.devision.tenant_id.id)
 
    template = 'inventory/products/measurement.html'
    context = {
        'measurement_list': measurement_list,
        'heading': 'List of Measurements',
        'pageview': 'Unit of Measurement',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_measuremnt',raise_exception = True)
def add_measurement(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = MeasurementForm(request.POST,request=request)
        if form.is_valid():
            name = form.cleaned_data['name']
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            measurement = Unit_of_Measurement.objects.get_or_create(name=name.title(),tenant_id=tenant_id)
            messages.info(request,'Unit of Measurement Saved')
            return redirect('inventory:measurement-list')
    else:
        form = MeasurementForm(request=request)

    template = 'inventory/products/create-measurement.html'
    context = {
        'form':form,
        'heading': 'New Unit of Measurement',
        'pageview': 'List of Unit of Measurement',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_update_measuremnt',raise_exception = True)
def edit_measurement(request,measurement_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    measurement=Unit_of_Measurement.objects.get(id=measurement_id)
    if request.method == 'POST':
        form = MeasurementForm(request.POST,instance=measurement,request=request)
        if form.is_valid():
            measurement=form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            measurement.tenant_id =tenant_id
            measurement.save()
            messages.info(request,'Unit of Measurement Updated')
            return redirect('inventory:measurement-list')
    else:
        form = MeasurementForm(instance=measurement,request=request)

    template = 'inventory/products/create-measurement.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Unit of Measurement',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_delete_measuremnt',raise_exception = True)
def delete_measurement(request,measurement_id):
    measurement=Unit_of_Measurement.objects.get(id=measurement_id)
    measurement.delete()
    messages.error(request,'Unit of Measurement Deleted')
    return redirect('inventory:measurement-list')
   
@login_required(login_url='authentication:login')
def measurement_upload(request):
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
                MeasureThread(dbframe).start()
                messages.success(request,'Unit of Measurement Data Upload Started')
            
            else:
                messages.error(request, 'File not found.')
            return redirect('inventory:measurement-list')
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
