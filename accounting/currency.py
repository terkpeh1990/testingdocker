# from msilib.schema import Error
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from .upload_thread import *
import pandas as pd
from tablib import Dataset
from django.core.files.storage import FileSystemStorage
from appsystem.models import *
from authentication.forms import *
import os 



@login_required(login_url='authentication:login')
@permission_required('accounting.custom_view_chart_of_accounts',raise_exception = True)
def currency(request):
    
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    currency_list = Currency.objects.all()
    template = 'accounting/currency/currency.html'
    context = {
        'currency_list': currency_list,
        'heading': 'List of Currencies',
        'pageview': 'Currency',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts',raise_exception = True)
def add_currency(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            symbol = form.cleaned_data['symbol']
            rate = form.cleaned_data['rate']
            currency = Currency.objects.get_or_create(name=name.title(),symbol=symbol.upper(),rate=rate)
            messages.info(request,'Currency Saved')
            return redirect('accounting:currency-list')
    else:
        form =  CurrencyForm()

    template = 'accounting/currency/create-currency.html'
    context = {
        'form':form,
        'heading': 'Currency',
        'pageview': 'List of Currency',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts',raise_exception = True)
def edit_currency(request,currency_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    currency=Currency.objects.get(id=currency_id)
    if request.method == 'POST':
        form = CurrencyForm(request.POST,instance=currency)
        if form.is_valid():
            form.save()
            messages.info(request,'Devision Updated')
            return redirect('accounting:currency-list')
    else:
        form = CurrencyForm(instance=currency)

    template = 'accounting/currency/create-currency.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Currencies',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts')
def delete_currency(request,currenncy_id):
    currency=Currency.objects.get(id=currenncy_id)
    currency.delete()
    messages.error(request,'Currency Deleted')
    return redirect('accounting:currency-list')


@login_required(login_url='authentication:login')
def uploads_currency(request):
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
                CurrencyThread(dbframe).start()
                messages.success(request,'Currency Data Upload Started')
                # return redirect('accounting:currency-list')
            else:
                messages.error(request, 'File not found.')

            return redirect('accounting:currency-list')
                
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
