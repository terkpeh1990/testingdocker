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
@permission_required('fixedassets.custom_create_source_of_fundings')
def funding(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    funding_list = SourceOfFunding.objects.all()
    template = 'fixedassets/funding/funding.html'
    context = {
        'funding_list': funding_list,
        'heading': 'List of funding',
        'pageview': 'Funding',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_source_of_fundings')
def add_funding(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = SourceOfFundingForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            funding = form.cleaned_data['funding']
            SourceOfFunding.objects.get_or_create(code=code.title(),funding=funding.title())
            messages.info(request,'Funding Saved')
            return redirect('fixedassets:funding-list')
    else:
        form = SourceOfFundingForm()

    template = 'fixedassets/funding/create-funding.html'
    context = {
        'form':form,
        'heading': 'New Funding',
        'pageview': 'List of Funding',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_source_of_fundings')
def edit_funding(request,funding_id):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    funding=SourceOfFunding.objects.get(id=funding_id)
    if request.method == 'POST':
        form = SourceOfFundingForm(request.POST,instance=funding)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Funding Updated')
            return redirect('fixedassets:funding-list')
    else:
        form = SourceOfFundingForm(instance=funding)

    template = 'fixedassets/funding/create-funding.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Funding',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('fixedassets.custom_create_source_of_fundings')
def delete_funding(request,funding_id):
    funding=SourceOfFunding.objects.get(id=funding_id)
    funding.delete()
    messages.error(request,'Funding Deleted')
    return redirect('fixedassets:funding-list')
   
@login_required(login_url='authentication:login')
def funding_upload(request):
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
                DataUploadThread(dbframe,action='funding').start()
                messages.success(request,'Funding Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('fixedassets:funding-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
