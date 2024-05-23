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
from company.models import *





@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_pv')
def banktype(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    bank_list = BankAccountsType.objects.all()
    template = 'accounting/banktype/bank.html'
    context = {
        'bank_list': bank_list,
        'heading': 'List of Bank Account Type',
        'pageview': 'Bank Accounts Type',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_pv')
def add_banktype(request):
   
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = BanktypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            banktype = BankAccountsType.objects.get_or_create(name=name.title())
            messages.info(request,'Bank Account Type Saved')
            return redirect('accounting:banktype-list')
    else:
        form = BanktypeForm()

    template = 'accounting/banktype/create-banktype.html'
    context = {
        'form':form,
        'heading': 'New Bank  Account Type',
        'pageview': 'List of Bank Account Type',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_pv')
def edit_banktype(request,banktypeid_id):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    banktype=BankAccountsType.objects.get(id=banktypeid_id)
    if request.method == 'POST':
        form = BanktypeForm(request.POST,instance=banktype)
        if form.is_valid():
            bank = form.save()
            messages.info(request,'Bank Account type  Updated')
            return redirect('accounting:banktype-list')
    else:
        form = BanktypeForm(instance=banktype)

    template = 'accounting/banktype/create-banktype.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Brands',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_pv')
def assign_banktype(request):
    bank= BankAccountsType.objects.all()
    sub_devision= Sub_Devision.objects.all()
    for sun in sub_devision:
        for b in bank:
            SubDevisionAccountType.objects.get_or_create(bankaccounttype=b ,sub_division = sun)
    messages.info(request,'Bank acoount type Assigned Successfully')
    return redirect('accounting:banktype-list')
   
@login_required(login_url='authentication:login')
def banktype_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            
            # Get the complete path to the uploaded file
            file_path = os.path.join(fs.location, filename)
            
            if os.path.exists(file_path):  # Check if the file exists
                empexceldata = pd.read_excel(file_path)
                dbframe = empexceldata
                BanktypeThread(dbframe).start()
                messages.success(request, 'Bank Account Type Data Uploaded Successfully')
                return redirect('accounting:banktype-list')
            else:
                messages.error(request, 'File not found.')
    else:
        form = UploadFileForm()
    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
   
@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_pv')
def delete_banktype(request):
    bank=BankAccountsType.objects.all()
    bank.delete()
    messages.error(request,'Bank acoount type Deleted')
    return redirect('accounting:banktype-list')