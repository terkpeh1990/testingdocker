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
from django.views.generic.list import ListView
from .filters import *
from .tasks import *
import json
from django.core import serializers
from fixedassets.models import FixedAsset
from fixedassets.forms import AssetsAssignmentForm
from authentication.permission import *




@login_required(login_url='authentication:login')
@permission_required('inventory.custom_view_requisition',raise_exception = True)
def personnalrequisition(request):
    if request.user.is_superuser:
        requisition_list = Requisition.objects.all()
        app_model = Companymodule.objects.all()
    else:
        
        requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id,staff = request.user)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    template = 'inventory/requisition/requisition-list.html'
    context = {
        'requisition_list': requisition_list,
        'heading': 'List of Requisition',
        'pageview': 'Requisition',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_approve_requisition',raise_exception = True)
def pendingrequisition(request):
    if request.user.is_superuser:
        requisition_list = Requisition.objects.filter(status="Pending")
        app_model = Companymodule.objects.all()
    else:
        print(request.user)
       
        requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id,staff__sub_division = request.user.sub_division,status="Pending")
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    template = 'inventory/requisition/requisition-list.html'
    context = {
        'requisition_list': requisition_list,
        'heading': 'List of Requisition',
        'pageview': 'Requisition',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_approve_capital_requisition',raise_exception = True)
def awaitingcapitalrequisition(request):
    if request.user.is_superuser:
        requisition_list = Requisition.objects.filter(classification="Capital",status="Awaiting Approval")
        app_model = Companymodule.objects.all()
    else:
        requisition_list = Requisition.objects.filter(classification="Capital",tenant_id=request.user.devision.tenant_id.id,status="Awaiting Approval")
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    template = 'inventory/requisition/requisition-list.html'
    context = {
        'requisition_list': requisition_list,
        'heading': 'List of Requisition',
        'pageview': 'Requisition',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_approve_consumable_requisition',raise_exception = True)
def awaitingconsumablerequisition(request):
    if request.user.is_superuser:
        requisition_list = Requisition.objects.filter(classification="Consumables",status="Awaiting Approval")
        app_model = Companymodule.objects.all()
    else:
    
        requisition_list = Requisition.objects.filter(classification="Consumables",tenant_id=request.user.devision.tenant_id.id,status="Awaiting Approval")
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    template = 'inventory/requisition/requisition-list.html'
    context = {
        'requisition_list': requisition_list,
        'heading': 'List of Requisition',
        'pageview': 'Requisition',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_issue_requisition',raise_exception = True)
def requisitionissue(request):
    if request.user.is_superuser:
        requisition_list = Requisition.objects.filter(status="Approved")
        app_model = Companymodule.objects.all()
    else:
    
        requisition_list = Requisition.objects.filter(status="Approved")
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    template = 'inventory/requisition/requisition-list.html'
    context = {
        'requisition_list': requisition_list,
        'heading': 'List of Requisition',
        'pageview': 'Requisition',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_view_requisition',raise_exception = True)
def allrequisition(request):
    if request.user.is_superuser:
        requisition_list = Requisition.objects.all()
        app_model = Companymodule.objects.all()
    else:
        requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    template = 'inventory/requisition/requisition-list.html'
    context = {
        'requisition_list': requisition_list,
        'heading': 'List of Requisition',
        'pageview': 'Requisition',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_requisition',raise_exception = True)
def add_requisition(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = RequisitionForm(request.POST,request=request)
        if form.is_valid():
            requisition = form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            requisition.tenant_id = tenant_id
            requisition.staff = request.user
            requisition.devision = request.user.devision
            requisition.sub_division = request.user.sub_division
            requisition.save()
            messages.info(request,'Requisition Initiated, Please add Products')
            return redirect('inventory:add-requisition-details' , requisition.id)
    else:
        form = RequisitionForm(request=request)

    template = 'inventory/requisition/create-requisition.html'
    context = {
        'form':form,
        'heading': 'New Requisition',
        'pageview': 'List of Requisisition',
        'app_model':app_model
    }
    return render(request,template,context)

# @permission_required(['inventory.custom_create_requisition','inventory.custom_approve_capital_requisition','inventory.custom_approve_consumable_requisition','inventory.custom_approve_requisition'],raise_exception = True)
def add_requisition_detail(request,requisition_id):
    requisition= Requisition.objects.get(id=requisition_id)
    detail = Requisition_Details.objects.filter(requisition_id=requisition.id)
   
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        product = Products.objects.filter(type_of_product=requisition.classification)
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        product = Products.objects.filter(tenant_id = request.user.devision.tenant_id.id,type_of_product=requisition.classification)
    if request.method == 'POST':
        form = RequisitionDetailForm(request.POST)
        prod = request.POST.get("product")
        a,_ = prod.split('-----')
        if form.is_valid():
            tenant =request.user.devision.tenant_id.id
            inven = Inventory.objects.get(product_id__name = a,tenant_id=tenant)
            quantity  = form.cleaned_data['quantity']
            Requisition_Details.objects.get_or_create(requisition_id=requisition,product_id=inven.product_id,quantity=quantity)
            messages.info(request,'Item added')
            return redirect('inventory:add-requisition-details' , requisition.id)
    else:
        form = RequisitionDetailForm()

    template = 'inventory/requisition/create-requisition-detail.html'
    context = {
        'form':form,
        'heading': 'New Requisition',
        'pageview': 'List of Requisition',
        'app_model':app_model,
        'detail':detail,
        'requisition':requisition,
        'product':product,
        
    }
    return render(request,template,context)


login_required(login_url='authentication:login')
def edit_requisition_detail(request,requisition_id):
    requisitions = Requisition_Details.objects.get(id=requisition_id)
    requisition = Requisition.objects.get(id=requisitions.requisition_id.id)
    detail = Requisition_Details.objects.filter(requisition_id=requisition.id)
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        product = Products.objects.filter(type_of_product=requisition.classification)
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        product = Products.objects.filter(tenant_id = request.user.devision.tenant_id.id,type_of_product=requisition.classification)
    if request.method == 'POST':
        form = RequisitionDetailForm(request.POST,instance=requisitions)
        prod = request.POST.get("product")
        if form.is_valid():
            tenant =request.user.devision.tenant_id.id
            inven = Inventory.objects.get(product_id__name = prod,tenant_id=tenant)
            product_id = product_id=inven.product_id
            quantity  = form.cleaned_data['quantity']
            
            requisitions.product_id = product_id
            requisitions.quantity = quantity
            requisitions.requisition_id =requisition
            requisitions.save()
            messages.info(request,'Item Updated')
            return redirect('inventory:add-requisition-details' , requisition.id)
    else:
        form = RequisitionDetailForm(instance=requisitions)

    template = 'inventory/requisition/update-requisition-detail.html'
    context = {
        'form':form,
        'heading': 'Update Requisition',
        'pageview': 'List of Requisition',
        'app_model':app_model,
        'detail':detail,
        'product':product,
        'requisition':requisition ,
        'item':requisitions
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_requisition',raise_exception = True)
def delete_requisition_item(request,requisition_id):
    requisition= Requisition_Details.objects.get(id=requisition_id)
    req = requisition.requisition_id.id
    requisition.delete()
    messages.error(request,'Item Deleted')
    return redirect('inventory:add-requisition-details', req)

login_required(login_url='authentication:login')
@permission_required('inventory.custom_update_requisition',raise_exception = True)
def edit_requisition(request,requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = RequisitionForm(request.POST,instance=requisition ,request=request)
        if form.is_valid():
            requisitions=form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            requisitions.tenant_id = tenant_id
            requisitions.staff = request.user
            requisitions.devision = request.user.devision
            requisitions.sub_division = request.user.sub_division
            requisitions.save()
            messages.info(request,'Requisition Updated')
            return redirect('inventory:add-requisition-details',requisition.id)
    else:
        form = RequisitionForm(instance=requisition ,request=request)

    template = 'inventory/requisition/create-requisition.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Requisition',
        'app_model':app_model
    }
    return render(request,template,context)

def delete_reqisition(request,requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    requisition.delete()
    messages.error(request,'Requisition Deleted')
    return redirect('inventory:personnal-requisition-list')

def send_notification_reqisition(request,requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    PendingThread(requisition).start()
    requisition.release =True
    requisition.save()
    messages.success(request,'Requisition Sent For Approval')
    return redirect('inventory:personnal-requisition-list')

def reverse_requisition(request,requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.user.has_perm('inventory.custom_approve_capital_requisition') or  request.user.has_perm('inventory.custom_approve_consumable_requisition'):
            requisition.status = "Awaiting Approval"
    else:
        requisition.status = "Pending"
    requisition.save()
    messages.info(request,'Certification Transaction Reversed')
    return redirect('inventory:add-requisition-details',requisition.id)

def cancel_requisition(request,requisition_id):
    admin = ['Pending','Approved']
    requisition = Requisition.objects.get(id=requisition_id)
    detail = Requisition_Details.objects.filter(requisition_id=details.id)
    if detail.filter(approval = 'Pending').exists() and request.user.has_perm('inventory.custom_approve_requisition'):
        messages.success(request,'You Must Cancel Each Individual Items')
        return redirect('inventory:add-requisition-details',requisition.id)
    elif detail.filter(approval__in= admin).exists() and request.user.has_perm('inventory.custom_approve_requisition'):
        messages.success(request,'You Must Approve or Cancel Each Individual Items')
        return redirect('inventory:add-requisition-details',requisition.id)
    else:    
        requisition.status="Cancelled"
        requisition.save()
        messages.error(request,'Requisition Cancelled')
    return redirect('inventory:add-requisition-details',requisition.id)



login_required(login_url='authentication:login')
# @permission_required(['inventory.custom_approve_requisition','inventory.custom_approve_capital_requisition','inventory.custom_approve_consumable_requisition'],raise_exception = True)
def approve_requisition(request,requisition_id):
    admin = ['Pending','Approved']
    requisition = Requisition.objects.get(id=requisition_id)
    detail = Requisition_Details.objects.filter(requisition_id=requisition.id)
    if detail.filter(approval = 'Pending').exists() and request.user.has_perm('inventory.custom_approve_requisition'):
        messages.error(request,'You Must Approve  Each Individual Items')
        return redirect('inventory:add-requisition-details',requisition.id)
    elif detail.filter(approval = 'Approved').exists()  and (request.user.has_perm('inventory.custom_approve_capital_requisition') or  request.user.has_perm('inventory.custom_approve_consumable_requisition')) :
        messages.error(request,'You Must Approve or Cancel Each Individual Items')
        return redirect('inventory:add-requisition-details',requisition.id)
    elif detail.filter(approval = 'Authorized').exists()  and request.user.has_perm('inventory.custom_issue_requisition')  :
        messages.error(request,'You Must Issue Each Individual Items')
        return redirect('inventory:add-requisition-details',requisition.id)
    else:    
        if request.user.has_perm('inventory.custom_approve_capital_requisition') or  request.user.has_perm('inventory.custom_approve_consumable_requisition'):
            requisition.status = "Approved"
            ApprovedThread(requisition).start()
            messages.success(request, "Requisition Has been sent to Stores For Issuing")
            requisition.save()
        elif request.user.has_perm('inventory.custom_issue_requisition'):
            requisition.status = "Issued"
            StoresThread(requisition).start()
            messages.success(request, "Requisition Has been Issued")
            requisition.save()

        else :
            requisition.status = "Awaiting Approval"
            AwaitingThread(requisition).start()
            messages.success(request, "Requisition Has been sent to Administration for approval")
            requisition.save()
    return redirect('inventory:add-requisition-details',requisition.id)


login_required(login_url='authentication:login')
@permission_required('inventory.custom_approve_requisition',raise_exception = True)    
def approve_individual_items(request,requisition_id):
    details = Requisition_Details.objects.get(id=requisition_id)
    details.approval = 'Approved'
    details.save()
    messages.success(request,'Item approved')
    return redirect('inventory:add-requisition-details', details.requisition_id)

login_required(login_url='authentication:login')
# @permission_required(['inventory.custom_approve_capital_requisition','inventory.custom_approve_consumable_requisition'],raise_exception = True)
def approve_quantity(request,requisition_id):
    detail = Requisition_Details.objects.get(id=requisition_id)
    item_inventory = Inventory.objects.get(product_id = detail.product_id)
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity_approved']
            if qty > item_inventory.avialable_quantity:
                messages.error(request, "Qantity approved cannot be more than" + " " + str(item_inventory.avialable_quantity))
                return redirect('inventory:approve-requisition-quantity', detail.id)
            else:
                detail.quantity_approved = form.cleaned_data['quantity_approved']
                detail.save()
                messages.success(request,"Approved Quantity Entered")
                return redirect('inventory:add-requisition-details', detail.requisition_id)
    else:
        
        form = QuantityForm()
    template = 'inventory/requisition/approve-quantity.html'
    context = {
        'form': form,
        'item_inventory': item_inventory,
        
        'detail':detail,
        }
    return render(request, template, context)


def reject_individual_items(request,requisition_id):
    details = Requisition_Details.objects.get(id=requisition_id)
    if request.user.has_perm('inventory.custom_approve_capital_requisition') or  request.user.has_perm('inventory.custom_approve_consumable_requisition'):
        details.approval = 'Admin Cancelled'
    else:
        details.approval = 'Cancelled'
    details.quantity_approved = 0
    details.save()
    messages.success(request,'Item Cancelled')
    return redirect('inventory:add-requisition-details', details.requisition_id)
        

def list_inventory(request,requisition_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    details = Requisition_Details.objects.get(id=requisition_id)
    requisition = Requisition.objects.get(id = details.requisition_id.id)
    inventory = Inventory.objects.get(product_id = details.product_id.id)
    if requisition.classification  == "Consumables":
        inventory_detail =  Inventory_Details.objects.filter(inventory_id = inventory,avialable_quantity__gt = 0).order_by('expiring_date')
        for i in inventory_detail:
            print(i.id)
    else:
        inventory_detail = FixedAsset.objects.filter(product=details.product_id.id ,status = 'Avialable')

    template = 'inventory/requisition/list-inventory.html'
    context = {
      
        'inventory': inventory,
        'inventory_detail':inventory_detail,
        'details':details,
        'requisition':requisition,
        'app_model':app_model,
        'heading': 'Issue Product',
        'pageview': 'List of Inventory Details',
        }
    return render(request, template, context)

login_required(login_url='authentication:login')
@permission_required('inventory.custom_issue_requisition',raise_exception = True)
def store_approve_quantity(request,requisition_id,detailbatch_id):
    detail = Requisition_Details.objects.get(id=requisition_id)
    item_inventory = Inventory.objects.get(product_id = detail.product_id)
    inventory_detail =  Inventory_Details.objects.get(batch_number = detailbatch_id,inventory_id=item_inventory.id)
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity_approved']
            if qty > item_inventory.avialable_quantity:
                messages.error(request, "Qantity approved cannot be more than" + " " + str(item_inventory.avialable_quantity))
                return redirect('inventory:approve-quantity', pk = detail.id)
            else:
                if request.user.has_perm('inventory.custom_issue_requisition'):
                    if form.cleaned_data['quantity_approved'] > detail.quantity_approved:
                        messages.error(request,"Quantiy Issued cannot be more than quantity approved")
                        return redirect('inventory:store-approve-quantity', detail.id)
                    else:
                        inventory_detail.quantity_requested += qty
                        inventory_detail.save()
                        item_inventory.avialable_quantity -= qty
                        item_inventory.save()
                        detail.quantity_issued = qty
                        detail.save()
                    messages.success(request,"Approved Issued Quantity Entered")
                    return redirect('inventory:list-inventory', detail.id)
    else:
        
        form = QuantityForm()
    template = 'inventory/requisition/approve-quantity.html'
    context = {
        'form': form,
        'item_inventory': item_inventory,
        
        'detail':detail,
        }
    return render(request, template, context)


login_required(login_url='authentication:login')
@permission_required('inventory.custom_issue_requisition',raise_exception = True)
def store_assets_issue(request,requisition_id,asset_id):
    detail = Requisition_Details.objects.get(id=requisition_id)
    item_inventory = Inventory.objects.get(product_id = detail.product_id)
    asset = FixedAsset.objects.get(id=asset_id)
    assets = Assigned_Assets.objects.filter(requisition_id=detail.requisition_id.id,tenant_id =detail.requisition_id.tenant_id.id )
    assets_count = assets.count()
    print(assets_count)
    if request.method == 'POST':
        form = AssetsAssignmentForm(request.POST,request=request)
        if form.is_valid():
            types = form.cleaned_data['usagetype']
            
            # try:
            #     assets = FixedAssetsAssignment.objects.filter(requisition_id=detail.requisition_id.id)
            #     assets_count = assets.count()
            #     print(assets_count)
            # except Assigned_Assets.DoesNotExist:
            #     assets_count = 0
  
            if request.user.has_perm('inventory.custom_issue_requisition') or request.user.has_perm('inventory.custom_create_user'):
                if detail.quantity_issued >= detail.quantity_approved:
                    messages.error(request,"Quantiy Issued cannot be more than" + str(detail.quantity_approved))
                    return redirect('inventory:store-assets-issue', detail.id,asset.id)
                else:
                    assignment = form.save(commit=False)
                    assignment.requisition = detail.requisition_id
                    assignment.status = 'Assigned'
                    assignment.asset = asset 
                    assignment.save()
                    item_inventory.avialable_quantity -= 1
                    item_inventory.save()
                    detail.quantity_issued +=1
                    detail.save()
                    asset.status = 'Assigned'
                    asset.costcenter = assignment.costcenter
                    asset.subcostcenter = assignment.subcostcenter
                    asset.location = assignment.subcostcenter.location
                    asset.user = assignment.user
                    asset.position = assignment.user.grade
                    asset.usagetype = assignment.usagetype
                    asset.currentstatus = 'In Use'
                    asset.save()
                messages.success(request,"Item Issued")
                return redirect('inventory:list-inventory', detail.id)
    else:
        
        form = AssetsAssignmentForm(request=request)
    template = 'fixedassets/assets/create-assign-asset.html'
    context = {
        'form': form,
        'item_inventory':item_inventory
        }
    return render(request, template, context)


