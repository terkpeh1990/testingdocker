# from msilib.schema import Error
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import *
from .forms import *
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from .upload_thread import *
import pandas as pd
from tablib import Dataset
from django.core.files.storage import FileSystemStorage
from appsystem.models import *
from authentication.forms import *
import os



@login_required(login_url='authentication:login')
@permission_required('company.custom_view_devision',raise_exception = True)
def devision(request):
    
    if request.user.is_superuser:
        devision_list = Devision.objects.all()
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        devision_list = Devision.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    template = 'company/devision.html'
    context = {
        'devision_list': devision_list,
        'heading': 'List of Cost Centers',
        'pageview': 'Cost Centers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('company.custom_view_devision',raise_exception = True)
def pending_devision(request):
 
    if request.user.is_superuser:
        devision_list = Devision.objects.filter(status=False)
        app_model = Companymodule.objects.all()
    else:
        devision_list = Devision.objects.filter(tenant_id = request.user.devision.tenant_id.id, status=False)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    template = 'company/devision.html'
    context = {
        'devision_list': devision_list,
        'heading': 'List of Cost Centers',
        'pageview': 'Cost Centers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('company.custom_create_devision',raise_exception = True)
def add_devision(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    if request.method == 'POST':
        form = DivisionForm(request.POST,request=request)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            tenant_id = form.cleaned_data['tenant_id']
            devision = Devision.objects.get_or_create(name=name.title(),code=code,tenant_id=tenant_id)
            messages.info(request,'Devision Saved')
            return redirect('company:devision-list')
    else:
        form =  DivisionForm(request=request)

    template = 'company/create-devision.html'
    context = {
        'form':form,
        'heading': 'New Cost Center',
        'pageview': 'List of Cost Centers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('company.custom_update_devision',raise_exception = True)
def edit_devision(request,devision_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    devision=Devision.objects.get(id=devision_id)
    if request.method == 'POST':
        form = DivisionForm(request.POST,instance=devision,request=request)
        if form.is_valid():
            form.save()
            messages.info(request,'Devision Updated')
            return redirect('company:devision-list')
    else:
        form = DivisionForm(instance=devision,request=request)

    template = 'company/create-devision.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Cost Centers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('company.custom_delete_devision',raise_exception = True)
def delete_devision(request,devision_id):
    devision=Devision.objects.get(id=devision_id)
    devision.delete()
    messages.error(request,'Devision Deleted')
    return redirect('company:devision-list')

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_devision',raise_exception = True)
def devision_detail(request,devision_id):
    if request.user.is_superuser:
            app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    devision=Devision.objects.get(id=devision_id)
    sub_devision = devision.sub_devisions.all()
    template = 'company/devision-detail-view.html'
    context = {
        'devision':devision,
        'sub_devision':sub_devision,
        'heading': 'List of Cost Centers',
        'pageview': 'Details'
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
def uploads_devision(request):
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
                DevisionThread(dbframe).start()
                messages.success(request,'Devision Data Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('company:devision-list')
     
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required(login_url='authentication:login')
@permission_required('company.custom_approve_devision',raise_exception = True)
def change_devision_status(request,devision_id):
    devision=Devision.objects.get(id=devision_id)
    if devision.status:
        devision.status = False
    else:
        devision.status = True
    devision.save()
    messages.info(request,'Devision Approved')
    return redirect('company:pending-devision-list')


@login_required(login_url='authentication:login')

def tag_devision(request,devision_id):
    devision=Devision.objects.get(id=devision_id)
    sub_devision= Sub_Devision.objects.filter(devision=devision.id)
    for i in sub_devision:
        i.tag = True
        i.save()
    messages.info(request,'Devision Taged')
    return redirect('company:pending-devision-list')