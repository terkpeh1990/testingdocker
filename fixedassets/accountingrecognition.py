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
@permission_required('fixedassets.custom_create_accounting_recognition')
def recognition(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    recognition_list = AccountingRecognition.objects.all()
    template = 'fixedassets/accrecgonition/recognition.html'
    context = {
        'recognition_list': recognition_list,
        'heading': 'List of Accounting Recognition',
        'pageview': 'Accounting Recognition',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_accounting_recognition')
def add_recognition(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = AccountingRecognitionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            classification = form.cleaned_data['classification']
            AccountingRecognition.objects.get_or_create(name=name.title(),classification=classification)
            messages.info(request,'Accounting Recognition Saved')
            return redirect('fixedassets:recognition-list')
    else:
        form = AccountingRecognitionForm()

    template = 'fixedassets/accrecgonition/create-recognition.html'
    context = {
        'form':form,
        'heading': 'New Accounting Recognisition',
        'pageview': 'List of Accounting Recognition',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_accounting_recognition')
def edit_recognition(request,recognition_id):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    recognition=AccountingRecognition.objects.get(id=recognition_id)
    if request.method == 'POST':
        form = AccountingRecognitionForm(request.POST,instance=recognition)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Accounting Recognition Updated')
            return redirect('fixedassets:recognition-list')
    else:
        form = AccountingRecognitionForm(instance=recognition)

    template = 'fixedassets/accrecgonition/create-recognition.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Accounting Recognition',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_accounting_recognition')
def delete_recognition(request,recognition_id):
    recognition=AccountingRecognition.objects.get(id=recognition_id)
    recognition.delete()
    messages.error(request,'Accounting Recognition Deleted')
    return redirect('fixedassets:recognition-list')
   
@login_required(login_url='authentication:login')
def recognition_upload(request):
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
                DataUploadThread(dbframe,action='recognition').start()
                messages.success(request,'Accounting Recognition Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('fixedassets:recognition-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
