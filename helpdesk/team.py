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
def team(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    team_list = Teams.objects.all()
    template = 'helpdesk/team/team.html'
    context = {
        'team_list': team_list,
        'heading': 'List of Teams',
        'pageview': 'Teams',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_team')
def add_team(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            classification = Teams.objects.get_or_create(name=name.title())
            messages.info(request,'Team Saved')
            return redirect('helpdesk:team-list')
    else:
        form = TeamForm()

    template = 'helpdesk/team/create-team.html'
    context = {
        'form':form,
        'heading': 'New Team',
        'pageview': 'List of Teams',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_team')
def edit_team(request,team_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    team=Teams.objects.get(id=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST,instance=team)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Team Updated')
            return redirect('helpdesk:team-list')
    else:
        form = TeamForm(instance=team)

    template = 'helpdesk/team/create-team.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Teams',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_team')
def delete_team(request,team_id):
    team=Teams.objects.get(id=team_id)
    team.delete()
    messages.error(request,'Team Deleted')
    return redirect('helpdesk:team-list')
   
@login_required(login_url='authentication:login')
def team_upload(request):
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
                DataUploadThread(dbframe,action='team').start()
                messages.success(request,'Team Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('helpdesk:team-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)