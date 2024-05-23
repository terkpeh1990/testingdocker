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
import os
from fixedassets.models import FixedAsset
from fixedassets.forms import AssetsAssignmentForm

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_report',raise_exception = True)
def allocation(request):
    if request.user.is_superuser:
        allocation_list = Allocation.objects.all()
        app_model = Companymodule.objects.all()
    else:
        
        allocation_list = Allocation.objects.filter(tenant_id=request.user.devision.tenant_id.id)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    template = 'inventory/allocation/allocation-list.html'
    context = {
        'allocation_list': allocation_list,
        'heading': 'List of Allocations',
        'pageview': 'Allocations',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_allocation',raise_exception = True)
def add_allocation(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            allocation = form.save(commit=False)
            tenant_id = request.user.devision.tenant_id
            allocation.tenant_id = tenant_id
            allocation.save()
            print(allocation.id)
            messages.info(request,'Allocation Initiated, Please add Destinations')
            return redirect('inventory:add-allocation-destination' , allocation.id)
    else:
        form = AllocationForm()

    template = 'inventory/allocation/create-allocation.html'
    context = {
        'form':form,
        'heading': 'New Allocation',
        'pageview': 'List of Allocations',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_allocation',raise_exception = True)
def add_allocation_destination(request,allocation_id):
    allocation = Allocation.objects.get(id=allocation_id)
    detail = Allocation_Destination.objects.filter(allocation_id=allocation.id,release=True)
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = AllocationDestinantionForm(request.POST,request=request)
        if form.is_valid():
            devision = form.cleaned_data['devision']
            classification = form.cleaned_data['classification'] 
            sub_devision = Sub_Devision.objects.filter(devision=devision)
            for i in sub_devision:
                Allocation_Destination.objects.get_or_create(devision=devision,sub_division=i,classification=classification,allocation_id=allocation)
            messages.info(request,'Destination Added, Please add Products')
            return redirect('inventory:add-allocation-destination' , allocation.id)
    else:
        form = AllocationDestinantionForm(request=request)

    template = 'inventory/allocation/create-allocation-destination.html'
    context = {
        'form':form,
        'heading': 'New Allocation',
        'pageview': 'List of Destinations',
        'app_model':app_model,
        'allocation':allocation,
        'detail':detail
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_allocation',raise_exception = True)
def edit_allocation_destination(request,allocation_id):
    details= Allocation_Destination.objects.get(id=allocation_id)
    allocation= Allocation.objects.get(id=details.allocation_id.id)
    detail = Allocation_Destination.objects.filter(allocation_id=allocation.id)
    
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = EditAllocationDestinantionForm(request.POST,instance=details,request=request)
        if form.is_valid():
            devision = form.cleaned_data['devision']
            sub_division = form.cleaned_data['sub_division']
            classification = form.cleaned_data['classification'] 
            print(classification)
            Allocation_Destination.objects.get_or_create(devision=devision,sub_division=sub_division,classification=classification,allocation_id=allocation)
            messages.info(request,'Destination Added, Please add Products')
            return redirect('inventory:allocation-destination' , allocation.id)
    else:
        form = EditAllocationDestinantionForm(instance=details,request=request)

    template = 'inventory/allocation/create-allocation-destination.html.html'
    context = {
        'form':form,
        'heading': 'New Allocation',
        'pageview': 'List of Destinations',
        'app_model':app_model,
        'allocation':allocation,
        'detail':detail
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_allocation',raise_exception = True)
def delete_allocation_destination(request,allocation_id):
    allocation = Allocation_Destination.objects.get(id=allocation_id)
    aa= allocation.allocation_id.id
    allocation.delete()
    messages.error(request,'Item Deleted')
    return redirect('inventory:add-allocation-destination' , aa)

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_allocation',raise_exception = True)
def release_allocation_destination(request,allocation_id):
    allocate = Allocation.objects.get(id=allocation_id)
    allocation = Allocation_Destination.objects.filter(allocation_id=allocate.id,release=True)
    for i in allocation:
        i.release = False
        i.save()
    messages.info(request,'Allocation For Region Done')
    return redirect('inventory:add-allocation-destination' , allocate)


def add_allocation_detail(request,destination_id):
    destination = Allocation_Destination.objects.get(id=destination_id)
    detail = Allocation_Details.objects.filter(destination_id=destination.id)
   
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        product = Products.objects.filter(type_of_product=requisition.classification)
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        product = Products.objects.filter(tenant_id = request.user.devision.tenant_id.id,type_of_product=destination.classification)
    if request.method == 'POST':
        form = RequisitionDetailForm(request.POST)
        prod = request.POST.get("product")
        a,_ = prod.split('-----')
        print(prod)
        if form.is_valid():
            tenant =request.user.devision.tenant_id.id
            inven = Inventory.objects.get(product_id__name = a,tenant_id=tenant)
            quantity  = form.cleaned_data['quantity']
            Allocation_Details.objects.get_or_create(destination_id=destination ,product_id=inven.product_id,quantity=quantity)
            messages.info(request,'Item added')
            return redirect('inventory:add-destination-item' , destination.id)
    else:
        form = RequisitionDetailForm()

    template = 'inventory/allocation/create-destination-item.html'
    context = {
        'form':form,
        'heading': 'New Allocation',
        'pageview': 'List of Destinations',
        'app_model':app_model,
        'detail':detail,
        'product':product,
        'destination':destination,
        
    }
    return render(request,template,context)



@login_required(login_url='authentication:login')
def allocation_detail_upload(request,destination_id):
    destination = Allocation_Destination.objects.get(id=destination_id)
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
                try:
                    for i in dbframe.itertuples():
                        tenant =request.user.devision.tenant_id.id
                        try:
                            inven = Inventory.objects.get(product_id__name = i.Products.title().strip(),tenant_id=tenant)
                            
                            Allocation_Details.objects.get_or_create(destination_id=destination ,product_id=inven.product_id,quantity=i.Quantity)
                        except Inventory.DoesNotExist:
                            pass
                    messages.info(request,'Allocation Items Uploaded')
                    return redirect('inventory:add-destination-item' , destination.id)  
                except IOError:
                    messages.error(request,'Allocation Data Upload Error')
                    return redirect('inventory:add-destination-item' , destination.id) 
                
            else:
                messages.error(request, 'File not found.')
            return redirect('inventory:add-destination-item' , destination.id)
             
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

@login_required(login_url='authentication:login')
# @permission_required('inventory.custom_delete_product')
def delete_destination_item(request,destination_id):
    allocation = Allocation_Details.objects.get(id=destination_id)
    allocation.delete()
    messages.error(request,'Item Deleted')
    return redirect('inventory:add-destination-item', allocation.destination_id.id)


def view_allocation_destination(request,allocation_id):
    destination_list = Allocation_Destination.objects.filter(allocation_id=allocation_id,finish=False)
    # detail = Allocation_Details.objects.filter(destination_id=destination.id,)
   
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
       
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
  
    template = 'inventory/allocation/view-destinations.html'
    context = {
        'heading': 'Allocation Detail',
        'pageview': 'List of Destinations',
        'app_model':app_model,
        
        'destination_list':destination_list,
        
    }
    return render(request,template,context)

def view_allocation_detail(request,destination_id):
    destination = Allocation_Destination.objects.get(id=destination_id)
    detail = Allocation_Details.objects.filter(destination_id=destination.id)
   
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()  
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    template = 'inventory/allocation/view-destination-items.html'
    context = {
        
        'heading': 'Destination Items',
        'pageview': 'List of Items',
        'app_model':app_model,
        'detail':detail,
        'destination':destination,
        
    }
    return render(request,template,context)

def allocation_list_inventory(request,item_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    details = Allocation_Details.objects.get(id=item_id)
  
    inventory = Inventory.objects.get(product_id = details.product_id.id )
    if details.destination_id.classification  == "Consumables":
        inventory_detail =  Inventory_Details.objects.filter(inventory_id = inventory,avialable_quantity__gt = 0).order_by('expiring_date')
    else:
        inventory_detail = FixedAsset.objects.filter(product_id=details.product_id.id ,status='Avialable')

    template = 'inventory/allocation/list-inventory.html'
    context = {
      
        'inventory': inventory,
        'inventory_detail':inventory_detail,
        'details':details,
        # 'requisition':requisition,
        'app_model':app_model,
        'heading': 'Issue Product',
        'pageview': 'List of Inventory Details',
        }
    return render(request, template, context)


login_required(login_url='authentication:login')
@permission_required('inventory.custom_issue_requisition',raise_exception = True)
def store_allocation_approve_quantity(request,item_id,detailbatch_id):
    detail = Allocation_Details.objects.get(id=item_id)
    item_inventory = Inventory.objects.get(product_id = detail.product_id)
    inventory_detail =  Inventory_Details.objects.get(batch_number = detailbatch_id,inventory_id=item_inventory.id)
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity_approved']
            if qty > item_inventory.avialable_quantity:
                messages.error(request, "Qantity approved cannot be more than" + " " + str(item_inventory.avialable_quantity))
                return redirect('inventory:store-allocation-approve-quantity', detail.id, detailbatch_id)
            else:
                if  qty > detail.quantity:
                        messages.error(request,"Quantiy Issued cannot be more than quantity approved")
                        return redirect('inventory:store-allocation-approve-quantity', detail.id,detailbatch_id)
                else:
                    inventory_detail.quantity_requested += qty
                    inventory_detail.save()
                    item_inventory.avialable_quantity += qty
                    item_inventory.save()
                    detail.quantity_issued += qty
                    detail.save()
                    messages.success(request,"Approved Issued Quantity Entered")
                    return redirect('inventory:allocation-list-inventory', detail.id)
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
# @permission_required('inventory.custom_issue_requisition')
def store_allocation_assets_issue(request,item_id,asset_id):
    detail = Allocation_Details.objects.get(id=item_id)
    item_inventory = Inventory.objects.get(product_id = detail.product_id)
    asset = FixedAsset.objects.get(id=asset_id)
    assets = Assigned_Assets.objects.filter(allocation_id=detail.destination_id.id,tenant_id = detail.destination_id.allocation_id.tenant_id.id )
    assets_count = assets.count()
    if request.method == 'POST':
        form = AssetsAssignmentForm(request.POST,request=request)
        if form.is_valid():
            types = form.cleaned_data['usagetype']
            if request.user.has_perm('inventory.custom_issue_requisition') or request.user.has_perm('inventory.custom_create_user'):
            
                if detail.quantity_issued >= detail.quantity:
                    messages.error(request,"Quantiy Issued cannot be more than" + str(detail.quantity))
                    return redirect('inventory:allocation-list-inventory', item_id)
                else:
                    assignment = form.save(commit=False)
                    assignment.allocation = detail.destination_id.allocation_id
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
                return redirect('inventory:allocation-list-inventory', item_id)
                
    else:
            
        form = AssetsAssignmentForm(request=request)
    template = 'fixedassets/assets/create-assign-asset.html'
    context = {
        'form': form,
        'item_inventory':item_inventory
        }
    return render(request, template, context)
    