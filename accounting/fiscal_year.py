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



@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_fisical_year',raise_exception = True)
def fiscalyear(request):
    
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    fiscalyear_list = Fiscal_year.objects.all()
    template = 'accounting/fiscalyear/fiscal-year.html'
    context = {
        'fiscalyear_list': fiscalyear_list,
        'heading': 'List of Fiscal Year',
        'pageview': 'Fiscal Year',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_fisical_year',raise_exception = True)
def add_fiscalyear(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    fiscalyears = Fiscal_year.objects.all().order_by('id')
    print(len(fiscalyears))
    if request.method == 'POST':       
        form = FiscalYearForm(request.POST)
        if form.is_valid():    
            if fiscalyears and len(fiscalyears) > 0:
                last_record = fiscalyears.latest('id')
                last_record.status = 'In Active'
                last_record.save()
                
            # else:
            #     lastyear = fiscalyears.reverse()[0]
            #     lastyear.status = 'In Active'
            #     lastyear.save()
            start=form.cleaned_data['start']
            fiscalyear=form.save(commit=False)
            fiscalyear.period = start.year
            fiscalyear.code = start.year
            fiscalyear.status= 'Open'
            fiscalyear.save()
            
            messages.info(request,'Fiscal Year Created')
            return redirect('accounting:fiscalyear-list')
    else:
        form =  FiscalYearForm()

    template = 'accounting/fiscalyear/create-fiscalyear.html'
    context = {
        'form':form,
        'heading': 'New',
        'pageview': 'List of Fiscal Year',
        'app_model':app_model
    }
    return render(request,template,context)



@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_fisical_year',raise_exception = True)
def edit_fiscalyear(request,fiscalyear_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    year = Fiscal_year.objects.get(id=fiscalyear_id)
    if request.method == 'POST':
        
        form = FiscalYearForm(request.POST,instance=year)
        if form.is_valid():
            start=form.cleaned_data['start']
            fiscalyear=form.save(commit=False)
            fiscalyear.period = start.year
            fiscalyear.code = start.year
            fiscalyear.save()
            messages.info(request,'Fiscal Year Updated')
            return redirect('accounting:fiscalyear-list')
    else:
        form =  FiscalYearForm(instance=year)

    template = 'accounting/fiscalyear/create-fiscalyear.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Fiscal Year',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_fisical_year',raise_exception = True)
def delete_fiscalyear(request,fiscalyear_id):
    year = Fiscal_year.objects.get(id=fiscalyear_id)
    year.delete()
    messages.error(request,'Fiscal Year Deleted')
    return redirect('accounting:fiscalyear-list')

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_fisical_year',raise_exception = True)
def activate_fiscalyear(request,fiscalyear_id):
    year = Fiscal_year.objects.get(id=fiscalyear_id)
    year.status = 'Active'
    year.save()
    messages.info(request,'Fiscal Year Activated')
    return redirect('accounting:fiscalyear-list')

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_fisical_year',raise_exception = True)
def deactivate_fiscalyear(request,fiscalyear_id):
    year = Fiscal_year.objects.get(id=fiscalyear_id)
    year.status = 'In Active'
    year.save()
    messages.error(request,'Fiscal Year Deactivated')
    return redirect('accounting:fiscalyear-list')

