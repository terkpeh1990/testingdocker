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
from django.db.models import Sum
from  .utils import *
from .sms_thread import *
from django.shortcuts import get_object_or_404
import inflect
import os 
# from django.shortcuts import get_object_or_404
 


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_imprest',raise_exception = True)
def manage_imprest(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    imprest_list = Imprest.objects.filter(raised_by=request.user.id)
    
    template = 'accounting/imprest/imprest-list.html'
    context = {
        'imprest_list': imprest_list,
        'heading': 'List of Imprest',
        'pageview': 'Imprest',
        'app_model':app_model
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_approve_imprest',raise_exception = True)
def pending_imprest(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    imprest_list = Imprest.objects.filter(sub_division=request.user.sub_division.id,status='Pending')
    
    template = 'accounting/imprest/imprest-list.html'
    context = {
        'imprest_list': imprest_list,
        'heading': 'List of Imprest',
        'pageview': 'Imprest',
        'app_model':app_model
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_certify_imprest',raise_exception = True)
def approved_imprest(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.user.has_perm('accounting.custom_headoffice'):
        imprest_list = Imprest.objects.filter(devision=request.user.devision.id,status='Approved')
    else:
        imprest_list = Imprest.objects.filter(sub_division=request.user.sub_division.id,status='Approved')
    
    template = 'accounting/imprest/imprest-list.html'
    context = {
        'imprest_list': imprest_list,
        'heading': 'List of Imprest',
        'pageview': 'Imprest',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_pay_imprest',raise_exception = True)
def certified_imprest(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.user.sub_division.tag:
        imprest_list = Imprest.objects.filter(devision=request.user.devision.id,status='Certified')
    else:
        imprest_list = Imprest.objects.filter(sub_division=request.user.sub_division.id,status='Certified')
    
    template = 'accounting/imprest/imprest-list.html'
    context = {
        'imprest_list': imprest_list,
        'heading': 'List of Imprest',
        'pageview': 'Imprest',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_pay_imprest',raise_exception = True)
def retire_imprest(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.user.sub_division.tag:
        imprest_list = Imprest.objects.filter(devision=request.user.devision.id,status='Paid')
    else:
        imprest_list = Imprest.objects.filter(sub_division=request.user.sub_division.id,status='Paid')
    
    template = 'accounting/imprest/imprest-list.html'
    context = {
        'imprest_list': imprest_list,
        'heading': 'List of Imprest',
        'pageview': 'Imprest',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_imprest',raise_exception = True)
def add_imprest(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    if request.method == 'POST':
        form = ImpressForm(request.POST)
        if form.is_valid():
            imprest = form.save(commit=False)
            imprest.raised_by = request.user
            imprest.devision = request.user.devision
            imprest.sub_division = request.user.sub_division
            imprest.raised_sub_division= request.user.sub_division.name
            imprest.raised_rank = request.user.grade.name
            imprest.save()
            by=f"Prepared By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
            Impresttimeline.objects.get_or_create(imprest_id=imprest,timeline_comment=by,staff=request.user)
            messages.info(request,'Impress Generated')
            return redirect('accounting:imprest-detail',imprest.id)
    else:
        form =  ImpressForm()

    template = 'accounting/imprest/create-imprest.html'
    context = {
        'form':form,
        'heading': 'Imprest',
        'pageview': 'List of Imprest',
        'app_model':app_model
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_imprest',raise_exception = True)
def edit_imprest(request,imprest_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    imprests = get_object_or_404(Imprest, pk=imprest_id)
    if request.method == 'POST':
        form = ImpressForm(request.POST,instance=imprests)
        if form.is_valid():
            imprest = form.save(commit=False)
            imprest.raised_by = request.user
            imprest.devision = request.user.devision
            imprest.sub_division = request.user.sub_division
            imprest.raised_sub_division= request.user.sub_division.name
            imprest.raised_rank = request.user.grade.name
            imprest.save()
            by=f"Updated By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
            Impresttimeline.objects.get_or_create(imprest_id=imprest,timeline_comment=by,staff=request.user)
            messages.info(request,'Impress Updated')
            return redirect('accounting:imprest-detail',imprest.id)
    else:
        form =  ImpressForm(instance=imprests)

    template = 'accounting/imprest/create-imprest.html'
    context = {
        'form':form,
        'heading': 'Imprest',
        'pageview': 'List of Imprest',
        'app_model':app_model
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_imprest',raise_exception = True)
def imprest_detail(request,imprest_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    imprest = get_object_or_404(Imprest, pk=imprest_id)
    currency = get_object_or_404(Currency,symbol='GHC')
    minutes = Impresttimeline.objects.filter(imprest_id = imprest.id ).order_by('-id')

    template = 'accounting/imprest/view_imprest.html'
    context = {
        
        'heading': 'Imprest',
        'pageview': 'List of Imprest',
        'app_model':app_model,
        'imprest':imprest,
        'currency':currency,
        'minutes':minutes
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
# @permission_required('dms.custom_can_create_pv_from_document',raise_exception = True)
def imprest_change_status(request,imprest_id):
    imprest = get_object_or_404(Imprest, pk=imprest_id)
    # ben = PaymentVoucherBeneficiary.objects.filter(pv_id=item)
    
    if request.user.has_perm('accounting.custom_approve_imprest') and imprest.status == 'Pending':
        imprest.status = 'Approved'
        by=f"Approved By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        Impresttimeline.objects.get_or_create(imprest_id=imprest,timeline_comment=by,staff=request.user)
        imprest.approved_by = request.user
        imprest.approved_rank =request.user.grade.name
        imprest.approved_sub_division = request.user.sub_division.name
        messages.info(request,'Imprest Approved')
        imprest.save()
        IprestApprovedNotificationThread(item=imprest).start()

    elif request.user.has_perm('accounting.custom_certify_imprest') and imprest.status == 'Approved':
        imprest.status = 'Certified'
        imprest.ammount_given = imprest.amount
        imprest.certified_by = request.user
        imprest.certified_rank =request.user.grade.name
        imprest.certified_sub_division = request.user.sub_division.name
        by=f"Certified By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        Impresttimeline.objects.get_or_create(imprest_id=imprest,timeline_comment=by,staff=request.user)
        messages.info(request,'Imprest Certified and Ready For Payment')
        imprest.save()
        IprestCertifiedNotificationThread(item=imprest).start()

    elif request.user.has_perm('accounting.custom_pay_imprest') and imprest.status == 'Certified':
        imprest.status = 'Paid'
        imprest.paid_by = request.user
        imprest.paid_rank =request.user.grade.name
        imprest.paid_sub_division = request.user.sub_division.name
        by=f"Paid By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        Impresttimeline.objects.get_or_create(imprest_id=imprest,timeline_comment=by,staff=request.user)
        messages.info(request,'Imprest Paid')
        imprest.save()
        IprestPaymentNotificationThread(item=imprest).start()

    elif request.user.has_perm('accounting.custom_pay_imprest') and imprest.status == 'Paid':
        imprest.status = 'Retired'
        imprest.paid_by = request.user
        imprest.paid_rank =request.user.grade.name
        imprest.paid_sub_division = request.user.sub_division.name
        by=f"Retired By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        Impresttimeline.objects.get_or_create(imprest_id=imprest,timeline_comment=by,staff=request.user)
        messages.info(request,'Imprest Retired')
        imprest.save()
        IprestPaymentNotificationThread(item=imprest).start()
    else:
        pass
    
    return redirect('accounting:imprest-detail',imprest.id)


@login_required(login_url='authentication:login')
# @permission_required('accounting.custom_pay_pv',raise_exception = True)
def notifyhod(request,imprest_id):
    imprest = get_object_or_404(Imprest, pk=imprest_id)
    if imprest.notifyhod:
        pass
    else:
        ImpresthodNotificationThread(imprest).start()
        imprest.notifyhod=True
        imprest.save()

    return redirect('accounting:manage-imprest')


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_pay_imprest',raise_exception = True)
def add_imprest_expense(request,imprest_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    imprest = get_object_or_404(Imprest, pk=imprest_id)
    if request.method == 'POST':
        form = ImpressactualExpenseForm(request.POST)
        if form.is_valid():
            imprest_expense = form.cleaned_data.get('actual_expense')
            imprest.actual_expense = imprest_expense
            imprest.save()
            
            by=f"Actual Expense of {imprest_expense} Recorded By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
            Impresttimeline.objects.get_or_create(imprest_id=imprest,timeline_comment=by,staff=request.user)
            messages.info(request,'Actual Expense Recorded')
            return redirect('accounting:imprest-detail',imprest.id)
    else:
        form =  ImpressactualExpenseForm()

    template = 'accounting/imprest/actualexpense.html'
    context = {
        'form':form,
        'heading': 'Imprest',
        'pageview': 'List of Imprest',
        'app_model':app_model,
    }
    return render(request,template,context)
