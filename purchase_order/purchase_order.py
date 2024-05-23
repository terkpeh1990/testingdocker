
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
# from .upload_thread import *
import pandas as pd
from tablib import Dataset
from django.core.files.storage import FileSystemStorage
from appsystem.models import *
from authentication.forms import *
from django.db.models import Count,Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404

import os 
from inventory.models import Products
from django.db.models import F
from purchase_order.models import *
from dms.models import DocumentProducts
from datetime import date
from inventory.models import Supplier_Products


@permission_required('purchase_order.custom_create_purchase_requisition',raise_exception = True)
@login_required(login_url='authentication:login')
def purchase_requisition(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        # supplier_list = Supplier.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    purchase_requisition_list = PurchaseRequisition.objects.all()
    template = 'purchaseorder/purchase_requisition/purchase-requisition.html'
    context = {
        'purchase_requisition_list': purchase_requisition_list,
        'heading': 'List of Purchase Requisition',
        'pageview': 'Purchase Requisition',
        'app_model':app_model
    }
    return render(request,template,context)


@permission_required('purchase_order.custom_create_purchase_requisition',raise_exception = True)
@login_required(login_url='authentication:login')
def create_purchase_order(request,document_product_id):
    today = date.today()
    document_product = DocumentProducts.objects.get(id=document_product_id)
    purchase_requisition,created = PurchaseRequisition.objects.get_or_create(purchase_requisition_date=today, user = request.user,product_id=document_product.product_id)
    document_product.status=True
    document_product.save()
    messages.info(request,'Purchase Requisiton Initiated')
    return redirect('purchaseorder:update-purchase-requisition',purchase_requisition.id)



@login_required(login_url='authentication:login')
@permission_required('purchase_order.custom_create_purchase_requisition',raise_exception = True)
def add_purchase_requisition(request,purchase_requisition_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    purchase_requisition = PurchaseRequisition.objects.get(id=purchase_requisition_id)
    print(purchase_requisition.product_id.id)
    if request.method == 'POST':
        form = PurchaseRquisitionForm(request.POST,instance=purchase_requisition)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            unit_price = form.cleaned_data['unit_price']
            purchase_requisition.quantity=quantity
            purchase_requisition.unit_price =unit_price
            purchase_requisition.save()
            aa = purchase_requisition.product_id.id
            print (aa)
            suppliers = Supplier_Products.objects.filter(product_id=aa)
            print(suppliers)
            for supplier in suppliers:
                print(supplier.product_id.name)
                PurchaseRequisition_Suppliers.objects.get_or_create(supplier_id=supplier.supplier_id,purchase_requisition_id=purchase_requisition)
            messages.info(request,'Purchase Requisition Created')
            return redirect('purchaseorder:purchase-requisition-detail',purchase_requisition.id)
    else:
        form = PurchaseRquisitionForm(instance=purchase_requisition)

    template = 'purchaseorder/purchase_requisition/create-purchase-requisition.html'
    context = {
        'form':form,
        'heading': 'New Purchase Requisition',
        'pageview': 'List of Purchase Requisitions',
        'app_model':app_model,
        'purchase_requisition':purchase_requisition
    }
    return render(request,template,context)


@permission_required('purchase_order.custom_view_purchase_requisition',raise_exception = True)
@login_required(login_url='authentication:login')
def view_purchase_requisition(request,purchase_requisition_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        # supplier_list = Supplier.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    purchase_requisition = PurchaseRequisition.objects.get(id=purchase_requisition_id)
    suppliers = PurchaseRequisition_Suppliers.objects.filter(purchase_requisition_id=purchase_requisition.id)
    template = 'purchaseorder/purchase_requisition/view-purchase-requisition.html'
    context = {
        'purchase_requisition': purchase_requisition,
        'heading': 'List of Purchase Requisition',
        'pageview': 'Purchase Requisition',
        'app_model':app_model,
        'suppliers':suppliers
    }
    return render(request,template,context)


def approve_purchase_requisition(request,purchase_requisition_id):
    requisition = PurchaseRequisition.objects.get(id=purchase_requisition_id)
    requisition.status = 'Approved'
    requisition.save()
    messages.info(request,'Requisition Approved')
    return redirect('purchaseorder:purchase-requisition-detail',requisition.id)


def cancel_purchase_requisition(request,purchase_requisition_id):
    requisition = PurchaseRequisition.objects.get(id=purchase_requisition_id)
    requisition.status = 'Cancelled'
    requisition.save()
    messages.info(request,'Requisition Cancelled')
    return redirect('purchaseorder:purchase-requisition-detail',requisition.id)


@login_required(login_url='authentication:login')
@permission_required('purchase_order.custom_create_purchase_requisition',raise_exception = True)
def add_quotation_requisition(request,quotation_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    supplier_quotation=PurchaseRequisition_Suppliers.objects.get(id=quotation_id)
  
    if request.method == 'POST':
        form = QoutationForm(request.POST,instance=supplier_quotation)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            supplier_quotation.amount = amount
            supplier_quotation.save()
            messages.info(request,'Supplier Quotation Recorded')
            return redirect('purchaseorder:purchase-requisition-detail',supplier_quotation.purchase_requisition_id.id)
    else:
        form = QoutationForm(instance=supplier_quotation)

    template = 'purchaseorder/purchase_requisition/quotation.html'
    context = {
        'form':form,
        'heading': 'New Purchase Requisition',
        'pageview': 'List of Purchase Requisitions',
        'app_model':app_model,
        'purchase_requisition':purchase_requisition
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('purchase_order.custom_create_purchase_requisition',raise_exception = True)
def approve_quotation_requisition(request,quotation_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    supplier_quotation=PurchaseRequisition_Suppliers.objects.get(id=quotation_id)
  
    if request.method == 'POST':
        form = DecisionRquisitionForm(request.POST,instance=supplier_quotation)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            supplier_quotation.reason = reason
            supplier_quotation.status ='Selected'
            supplier_quotation.purchase_requisition_id.supplier_id=supplier_quotation.supplier_id
            supplier_quotation.save()
            supplier_quotation.purchase_requisition_id.save()
            messages.info(request,'Supplier Selected')
            return redirect('purchaseorder:purchase-requisition-detail',supplier_quotation.purchase_requisition_id.id)
    else:
        form = DecisionRquisitionForm(instance=supplier_quotation)

    template = 'purchaseorder/purchase_requisition/reason.html'
    context = {
        'form':form,
        'heading': 'New Purchase Requisition',
        'pageview': 'List of Purchase Requisitions',
        'app_model':app_model,
        'purchase_requisition':purchase_requisition
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('purchase_order.custom_create_purchase_requisition',raise_exception = True)
def reject_quotation_requisition(request,quotation_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    supplier_quotation=PurchaseRequisition_Suppliers.objects.get(id=quotation_id)
  
    if request.method == 'POST':
        form = DecisionRquisitionForm(request.POST,instance=supplier_quotation)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            supplier_quotation.reason = reason
            supplier_quotation.status ='Rejected'
            supplier_quotation.save()
            messages.info(request,'Supplier Rejected')
            return redirect('purchaseorder:purchase-requisition-detail',supplier_quotation.purchase_requisition_id.id)
    else:
        form = DecisionRquisitionForm(instance=supplier_quotation)

    template = 'purchaseorder/purchase_requisition/reason.html'
    context = {
        'form':form,
        'heading': 'New Purchase Requisition',
        'pageview': 'List of Purchase Requisitions',
        'app_model':app_model,
        'purchase_requisition':purchase_requisition
    }
    return render(request,template,context)

def complete_supplier_selection(request,purchase_requisition_id):
    requisition = PurchaseRequisition.objects.get(id=purchase_requisition_id)
    requisition.release = True
    requisition.save()
    messages.info(request,'Supplier Selection Comfirmed')
    return redirect('purchaseorder:purchase-requisition-detail',requisition.id)

@login_required(login_url='authentication:login')
@permission_required('purchase_order.custom_create_lpo',raise_exception = True)
def create_lpo(request,purchase_requisition_id):
    requisition = PurchaseRequisition.objects.get(id=purchase_requisition_id)
    lpo,created = LocalPurchasingOrder.objects.get_or_create(user=request.user,product_id=requisition.product_id,quantity=requisition.quantity,unit_price=requisition.unit_price,total_amount=requisition.total_amount,supplier_id=requisition.supplier_id,purchase_requisition_id=requisition)
    requisition.status ='LPO Created'
    requisition.save()
    messages.info(request,'LPO Created')
    return redirect('purchaseorder:detail-lpo',lpo.id)


@login_required(login_url='authentication:login')
@permission_required('purchase_order.custom_view_lpo',raise_exception = True)
def view_lpo(request,lpo_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    lpo =  LocalPurchasingOrder.objects.get(id=lpo_id)
    template = 'purchaseorder/lpo/view-lpo.html'
    context = {
        
        'heading': 'New LPO',
        'pageview': 'List of LPO',
        'app_model':app_model,
        'lpo':lpo
    }
    return render(request,template,context)

@permission_required('purchase_order.custom_view_lpo',raise_exception = True)
@login_required(login_url='authentication:login')
def lpo(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        # supplier_list = Supplier.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    lpo_list = LocalPurchasingOrder.objects.all()
    template = 'purchaseorder/lpo/lpo_list.html'
    context = {
        'lpo_list': lpo_list,
        'heading': 'List of LPO',
        'pageview': 'Purchase Requisition',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('purchase_order.custom_approve_lpo',raise_exception = True)
def approve_lpo(request,lpo_id):
    lpo = LocalPurchasingOrder.objects.get(id=lpo_id)
    lpo.status = 'Approved'
    lpo.save()
    messages.info(request,'LPO Approved')
    return redirect('purchaseorder:detail-lpo',lpo.id)

@login_required(login_url='authentication:login')
@permission_required('purchase_order.custom_approve_lpo',raise_exception = True)
def cancel_lpo(request,lpo_id):
    lpo = LocalPurchasingOrder.objects.get(id=lpo_id)
    lpo.status = 'Cancelled'
    lpo.save()
    messages.info(request,'LPO Approved')
    return redirect('purchaseorder:detail-lpo',lpo.id)