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
@permission_required('company.custom_view_sub_devision',raise_exception = True)
def sub_devision(request):

    if request.user.is_superuser:
        sub_devision_list = Sub_Devision.objects.all()
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        sub_devision_list = Sub_Devision.objects.filter(devision__tenant_id=request.user.devision.tenant_id.id)
    template = 'company/sub_devision.html'
    context = {
        'sub_devision_list': sub_devision_list,
        'heading': 'List of Sub Cost Centers',
        'pageview': 'Sub Cost Centers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('company.custom_create_sub_devision',raise_exception = True)
def add_sub_devison(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = SubDivisionForm(request.POST,request=request)
        if form.is_valid():
            name = form.cleaned_data['name']
            devision = form.cleaned_data['devision']
            sub_devision =Sub_Devision.objects.get_or_create(name=name.title(),devision=devision)
            messages.info(request,'Sub Devision Saved')
            return redirect('company:sub_division-list')
    else:
        form = SubDivisionForm(request=request)

    template = 'company/create-sub_devision.html'
    context = {
        'form':form,
        'heading': 'New Sub Cost Center',
        'pageview': 'List of Sub Cost Centers',
        'app_model':app_model,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('company.custom_update_sub_devision',raise_exception = True)
def edit_sub_devison(request,subdivision_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    sub_devison=Sub_Devision.objects.get(id=subdivision_id)
    if request.method == 'POST':
        form = SubDivisionForm(request.POST,instance=sub_devison,request=request)
        if form.is_valid():
            form.save()
            messages.info(request,'District Updated')
            return redirect('company:sub_division-list')
    else:
        form = SubDivisionForm(instance=sub_devison,request=request)

    template = 'company/create-sub_devision.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Sub Cost Centers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('company.custom_delete_sub_devision',raise_exception = True)
def delete_sub_devision(request,subdivision_id):
    sub_devison=Sub_Devision.objects.get(id=subdivision_id)
    sub_devison.delete()
    messages.error(request,'Sub District Deleted')
    return redirect('company:sub_division-list')

   
@login_required(login_url='authentication:login')
def uploads_sub_devision(request):
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
                Sub_DevisionThread(dbframe).start()
                messages.success(request,'Sub District Data Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('company:sub_division-list')
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


   
