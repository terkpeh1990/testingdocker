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
@permission_required('fixedassets.custom_create_classification')
def classification(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    classification_list = Classification.objects.all()
    template = 'fixedassets/classification/classification.html'
    context = {
        'classification_list': classification_list,
        'heading': 'List of Classifications',
        'pageview': 'Classification',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_classification')
def add_classification(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = ClassificationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            classification = Classification.objects.get_or_create(name=name.title())
            messages.info(request,'Classification Saved')
            return redirect('fixedassets:classification-list')
    else:
        form = ClassificationForm()

    template = 'fixedassets/classification/create-classification.html'
    context = {
        'form':form,
        'heading': 'New Classification',
        'pageview': 'List of Classification',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_classification')
def edit_classification(request,classification_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    classification=Classification.objects.get(id=classification_id)
    if request.method == 'POST':
        form = ClassificationForm(request.POST,instance=classification)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Classification Updated')
            return redirect('fixedassets:classification-list')
    else:
        form = ClassificationForm(instance=classification)

    template = 'fixedassets/classification/create-classification.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Classifications',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_classification')
def delete_classification(request,classification_id):
    classification=Classification.objects.get(id=classification_id)
    classification.delete()
    messages.error(request,'Classification Deleted')
    return redirect('fixedassets:classification-list')
   
@login_required(login_url='authentication:login')
def classification_upload(request):
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
                DataUploadThread(dbframe,action='classification').start()
                messages.success(request,'Classification Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('fixedassets:classification-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
