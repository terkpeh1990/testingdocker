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
import os



@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_Rank',raise_exception = True)
def grade(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    grade_list = Grade.objects.all()
    template = 'authentication/grade.html'
    context = {
        'grade_list': grade_list,
        'heading': 'List of Ranks',
        'pageview': 'Ranks',
        'app_model':app_model,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_create_rank',raise_exception = True)
def add_grade(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            grade = Grade.objects.get_or_create(name=name.title(),tenant_id=request.user.tenant_id)
            messages.info(request,'Grade Saved')
            return redirect('authentication:grade-list')
    else:
        form = GradeForm()

    template = 'authentication/create-grade.html'
    context = {
        'form':form,
        'heading': 'New Rank',
        'pageview': 'List of Ranks',
        'app_model':app_model,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_update_rank',raise_exception = True)
def edit_grade(request,grade_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    grade=Grade.objects.get(id=grade_id)
    if request.method == 'POST':
        form = GradeForm(request.POST,instance=grade)
        if form.is_valid():
            aa=form.save()
            aa.tenant_id =request.user.tenant_id
            aa.save()
            messages.info(request,'Grade Updated')
            return redirect('authentication:grade-list')
    else:
        form = GradeForm(instance=grade)

    template = 'authentication/create-grade.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Ranks',
        'app_model':app_model,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_delete_rank',raise_exception = True)
def delete_grade(request,grade_id):
    grade=Grade.objects.get(id=grade_id)
    grade.delete()
    messages.error(request,'Grade Deleted')
    return redirect('authentication:grade-list')
   
@login_required(login_url='authentication:login')
def uploads(request):
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
                GradeThread(dbframe).start()
                messages.success(request,'Grad Data Uploaded Successfully')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('authentication:grade-list')
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
