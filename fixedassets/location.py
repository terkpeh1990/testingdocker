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
@permission_required('fixedassets.custom_create_location')
def location(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    location_list = Location.objects.all()
    template = 'fixedassets/location/location.html'
    context = {
        'location_list': location_list,
        'heading': 'List of Location',
        'pageview': 'Location',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_location')
def add_location(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            location = form.cleaned_data['location']
            Location.objects.get_or_create(code=code.title(),location=location)
            messages.info(request,'Location Saved')
            return redirect('fixedassets:location-list')
    else:
        form = LocationForm()

    template = 'fixedassets/location/create-location.html'
    context = {
        'form':form,
        'heading': 'New Location',
        'pageview': 'List of Location',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_location')
def edit_location(request,location_id):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    location=Location.objects.get(id=location_id)
    if request.method == 'POST':
        form = LocationForm(request.POST,instance=location)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Location Updated')
            return redirect('fixedassets:location-list')
    else:
        form = LocationForm(instance=location)

    template = 'fixedassets/location/create-location.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Location',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_location')
def delete_location(request,location_id):
    location=Location.objects.get(id=location_id)
    location.delete()
    messages.error(request,'Location Deleted')
    return redirect('fixedassets:location-list')
   
@login_required(login_url='authentication:login')
def location_upload(request):
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
                DataUploadThread(dbframe,action='location').start()
                messages.success(request,'Location Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('fixedassets:location-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
