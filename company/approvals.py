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



@login_required(login_url='authentication:login')
@permission_required('authentication.custom_create_user')
def approval(request):
    
    if request.user.is_superuser:
        approval_list = Approvals.objects.all()
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        approval_list = Approvals.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    template = 'company/approval-list.html'
    context = {
        'approval_list': approval_list,
        'heading': 'List of Approvals',
        'pageview': 'Approvals',
        'app_model':app_model
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('authentication.custom_create_user')
def add_approval(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    if request.method == 'POST':
        form = ApprovalForm(request.POST,request=request)
        if form.is_valid():
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            user_id = form.cleaned_data['user_id']
            classification = form.cleaned_data['classification']
            type_of_approval = form.cleaned_data['type_of_approval']
            approval = Approvals.objects.get_or_create(tenant_id=tenant_id,user_id=user_id,classification=classification,type_of_approval=type_of_approval)
            messages.info(request,'Approval Saved')
            return redirect('company:approval-list')
    else:
        form =  ApprovalForm(request=request)

    template = 'company/create-approval.html'
    context = {
        'form':form,
        'heading': 'New Approval',
        'pageview': 'List of Approvals',
        'app_model':app_model
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('authentication.custom_create_user')
def edit_approval(request,approval_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    approval = Approvals.objects.get(id=approval_id)  
    if request.method == 'POST':
        form = ApprovalForm(request.POST,request=request,instance=approval)
        if form.is_valid():
            aprove= form.save(commit=False)

            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            approve.tenant_id=tenant_id
            approve.save()
            messages.info(request,'Approval updated')
            return redirect('company:approval-list')
    else:
        form =  ApprovalForm(request=request,instance=approval)

    template = 'company/create-approval.html'
    context = {
        'form':form,
        'heading': 'Update Approval',
        'pageview': 'List of Approvals',
        'app_model':app_model
    }
    return render(request,template,context) 


@login_required(login_url='authentication:login')
@permission_required('authentication.custom_create_user')
def delete_approval(request,approval_id):
    approval = Approvals.objects.get(id=approval_id)  
    approval.delete()
    messages.error(request,'Approval Deleted')
    return redirect('company:approval-list')

   
@login_required(login_url='authentication:login')
def uploads_approval(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            uploaded_file_url = fs.url(filename)              
            empexceldata = pd.read_excel(filename)        
            dbframe = empexceldata
            ApprovalThread(dbframe).start()
            messages.success(request,'Approval Data Upload Started')
            return redirect('company:approval-list')
                
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)