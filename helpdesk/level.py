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
@permission_required('helpdesk.custom_create_team')
def level(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    level_list = Level.objects.all()
    template = 'helpdesk/level/level.html'
    context = {
        'level_list': level_list,
        'heading': 'List of Levels',
        'pageview': 'Levels',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_team')
def add_level(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = LevelForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            level = Level.objects.get_or_create(name=name.title())
            messages.info(request,'Team Saved')
            return redirect('helpdesk:level-list')
    else:
        form = LevelForm()

    template = 'helpdesk/level/create-level.html'
    context = {
        'form':form,
        'heading': 'New Level',
        'pageview': 'List of Levels',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_team')
def edit_level(request,level_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    level=Level.objects.get(id=level_id)
    if request.method == 'POST':
        form = LevelForm(request.POST,instance=level)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Team Updated')
            return redirect('helpdesk:level-list')
    else:
        form = LevelForm(instance=level)

    template = 'helpdesk/level/create-level.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Levels',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_team')
def delete_level(request,level_id):
    level=Level.objects.get(id=level_id)
    level.delete()
    messages.error(request,'Level Deleted')
    return redirect('helpdesk:level-list')
   
@login_required(login_url='authentication:login')
def level_upload(request):
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
                DataUploadThread(dbframe,action='level').start()
                messages.success(request,'Level Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('helpdesk:level-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)