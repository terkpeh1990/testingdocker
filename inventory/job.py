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
import os



@login_required(login_url='authentication:login')
@permission_required('inventory.custom_view_job_certification',raise_exception = True)
def job_cert(request):
    if request.user.is_superuser:
        job_list = Job_Certification.objects.all()
        app_model = Companymodule.objects.all()
    else:
       
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        job_list = Job_Certification.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    template = 'inventory/job/job.html'
    context = {
        'job_list': job_list,
        'heading': 'List of Certifications',
        'pageview': 'Certification',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
def load_product(request):
    category = request.GET.get('category')
    product = Products.objects.filter(tenant_id=request.user.tenant_id,category_id=category).order_by('name')
    return render(request, 'inventory/products/product_dropdown_list.html', {'product': product})

@login_required(login_url='authentication:login')
@permission_required('inventory.custom_create_job_certification',raise_exception = True)
def add_job(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = JobForm(request.POST,request=request)
        if form.is_valid():
            certification_date = form.cleaned_data.get('certification_date')
            supplier_id =form.cleaned_data.get('supplier_id')
            classification = form.cleaned_data.get('classification')
            category = form.cleaned_data.get('category')
            product = form.cleaned_data.get('product')
            description = form.cleaned_data.get('description')
            note = form.cleaned_data.get('note')
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
            job,created = Job_Certification.objects.get_or_create(certification_date=certification_date,classification=classification,category=category,product=product,description=description,note=note,supplier_id=supplier_id,tenant_id=tenant_id)
            messages.info(request,'Certification Initiated, Please add or upload Products')
            return redirect('inventory:add-job-details' , job.id)
    else:
        form = JobForm(request=request)

    template = 'inventory/job/create-job.html'
    context = {
        'form':form,
        'heading': 'New Certification',
        'pageview': 'List of Certification',
        'app_model':app_model
    }
    return render(request,template,context)


def add_job_detail(request,job_id):
    job = Job_Certification.objects.get(id=job_id)
    detail = Job_detail.objects.filter(job_id=job.id)
    total = detail.count()
    total_accepted = detail.filter(status="Accepted").count()
    total_rejected = detail.filter(status="Rejected").count()
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        if job.classification.name == 'Land':
            form = JobLandForm(request.POST,request=request)
        elif job.classification.name == 'Buldings And Other Structures':
            form = JobBuildingForm(request.POST,request=request)
        elif job.classification.name == 'Transport Equipments':
            form = JobTransportForm(request.POST,request=request)
        elif job.classification.name == 'Outdoor Machinery And Equipments':
            form = JobOutdoorForm(request.POST,request=request)
        elif job.classification.name == 'Indoor':
            form = JobIndoorForm(request.POST,request=request)
        else:
            form =JobWIPForm(request.POST,request=request)


        if form.is_valid():
            asset = form.save(commit=False)
            asset.job_id =job
            asset.product = job.product
            asset.description = job.description
            asset.save()
            messages.info(request,'Item added')
            return redirect('inventory:add-job-details' , job.id)
    else:
        if job.classification.name == 'Land':
            form = JobLandForm(request=request)
        elif job.classification.name == 'Buldings And Other Structures':
            form = JobBuildingForm(request=request)
        elif job.classification.name == 'Transport Equipments':
            form = JobTransportForm(request=request)
        elif job.classification.name == 'Outdoor Machinery And Equipments':
            form = JobOutdoorForm(request=request)
        elif job.classification.name == 'Indoor':
            form = JobIndoorForm(request=request)
        else:
            form =JobWIPForm(request=request)
            
        
    if job.classification.name == 'Land':
        template = 'inventory/job/create-job-land.html'
    elif job.classification.name == 'Buldings And Other Structures':
        template = 'inventory/job/create-job-building.html'
    elif job.classification.name == 'Transport Equipments':
        template = 'inventory/job/create-job-transport.html'
    elif job.classification.name == 'Indoor':
        template = 'inventory/job/create-job-indoor.html'
    elif job.classification.name == 'Outdoor Machinery And Equipments':
        template = 'inventory/job/create-job-outdoor.html'
    else:
        template = 'inventory/job/create-job-wip.html'


    context = {
        'form':form,
        'heading': 'New Restock',
        'pageview': 'List of Restock',
        'app_model':app_model,
        'detail':detail,
        'job':job,
        'total':total,
        'total_accepted':total_accepted,
        'total_rejected':total_rejected
    }
    return render(request,template,context)


def edit_job_detail(request,job_id):
    jobs = Job_detail.objects.get(id=job_id)
    job = Job_Certification.objects.get(id=jobs.job_id.id)
    detail = Job_detail.objects.filter(job_id=job.id)
    total = detail.count()
    total_accepted = detail.filter(status="Accepted").count()
    total_rejected = detail.filter(status="Rejected").count()
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    if request.method == 'POST':
        if job.classification.name == 'Land':
            form = JobLandForm(request.POST,request=request,instance=jobs)
        elif job.classification.name == 'Buldings And Other Structures':
            form = JobBuildingForm(request.POST,request=request,instance=jobs)
        elif job.classification.name == 'Transport Equipments':
            form = JobTransportForm(request.POST,request=request,instance=jobs)
        elif job.classification.name == 'Outdoor Machinery And Equipments':
            form = JobOutdoorForm(request.POST,request=request,instance=jobs)
        elif job.classification.name == 'Indoor':
            form = JobIndoorForm(request.POST,request=request,instance=jobs)
        else:
            form =JobWIPForm(request.POST,request=request,instance=jobs)


        if form.is_valid():
            asset = form.save(commit=False)
            asset.job_id =job
            asset.product = job.product
            asset.description = job.description
            asset.save()
            messages.info(request,'Item added')
            return redirect('inventory:add-job-details' , job.id)
    else:
        if job.classification.name == 'Land':
            form = JobLandForm(request=request,instance=jobs)
        elif job.classification.name == 'Buldings And Other Structures':
            form = JobBuildingForm(request=request,instance=jobs)
        elif job.classification.name == 'Transport Equipments':
            form = JobTransportForm(request=request,instance=jobs)
        elif job.classification.name == 'Outdoor Machinery And Equipments':
            form = JobOutdoorForm(request=request,instance=jobs)
        elif job.classification.name == 'Indoor':
            form = JobIndoorForm(request=request,instance=jobs)
        else:
            form =JobWIPForm(request=request,instance=jobs)
            
        
    if job.classification.name == 'Land':
        template = 'inventory/job/create-job-land.html'
    elif job.classification.name == 'Buldings And Other Structures':
        template = 'inventory/job/create-job-building.html'
    elif job.classification.name == 'Transport Equipments':
        template = 'inventory/job/create-job-transport.html'
    elif job.classification.name == 'Indoor':
        template = 'inventory/job/create-job-indoor.html'
    elif job.classification.name == 'Outdoor Machinery And Equipments':
        template = 'inventory/job/create-job-outdoor.html'
    else:
        template = 'inventory/job/create-job-wip.html'
   
    context = {
        'form':form,
        'heading': 'Update Certification',
        'pageview': 'List of Certification',
        'app_model':app_model,
        'detail':detail,
        'job':job,
        'item':jobs,
        'total':total,
        'total_accepted':total_accepted,
        'total_rejected':total_rejected
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
# @permission_required('inventory.custom_delete_product')
def delete_job_item(request,job_id):
    job= Job_detail.objects.get(id=job_id)
    job.delete()
    messages.error(request,'Item Deleted')
    return redirect('inventory:add-job-details', job.job_id.id )


@login_required(login_url='authentication:login')
@permission_required('inventory.custom_update_job_certification',raise_exception = True)
def edit_job(request,job_id):
    job = Job_Certification.objects.get(id=job_id)
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = JobForm(request.POST,instance=job ,request=request)
        if form.is_valid():
            restock=form.save(commit=False)
            if request.user.is_superuser:
                tenant_id = form.cleaned_data['tenant_id']
            else:
                tenant_id = request.user.devision.tenant_id
                
            restock.tenant_id = tenant_id
            restock.save()
            messages.info(request,'Restock Updated')
            return redirect('inventory:add-job-details',job.id)
    else:
        form = JobForm(instance=job ,request=request)

    template = 'inventory/job/create-job.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Restocks',
        'app_model':app_model
    }
    return render(request,template,context)


def delete_job(request,job_id):
    job = Job_Certification.objects.get(id=job_id)
    job.delete()
    messages.error(request,'Certification Deleted')
    return redirect('inventory:job-list')



@login_required(login_url='authentication:login')
def job_detail_upload(request,job_id):
    job = Job_Certification.objects.get(id=job_id)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            uploaded_file_url = fs.url(filename)  
            file_path = os.path.join(fs.location, filename) 
            if os.path.exists(file_path):           
                empexceldata = pd.read_excel(file_path)      
                dbframe = empexceldata
                try:
                    for i in dbframe.itertuples():
                        tenant =request.user.devision.tenant_id.id
                        try:
                            brand = Brands.objects.get(name=i.Brand.title().strip(),tenant_id=tenant)
                        except Brands.DoesNotExist:
                            brand = Brands.objects.create(name=i.Brand.title().strip(),tenant_id=tenant)
                        try:
                            inven = Inventory.objects.get(product_id__name = i.Products.title().strip(),tenant_id=tenant)
                            product_id=inven.product_id
                            
                            Job_detail.objects.get_or_create(job_id=job,product_id=product_id,brand_id=brand,serial_number=i.Serialnumber,description=i.Describtione,status=i.Status,funding=i.Funding)
                        except Inventory.DoesNotExist:
                            pass
                    messages.info(request,'Restock Data Uploaded')
                    return redirect('inventory:add-job-details',job.id)  
                except IOError:
                    messages.error(request,'Restock Data Upload Error')
                    return redirect('inventory:add-job-details',job.id)  
            else:
                messages.error(request, 'File not found.')
            return redirect('inventory:add-job-details',job.id) 
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def cancel_job(request,job_id):
    job = Job_Certification.objects.get(id=job_id)
    job.status="Cancelled"
    job.save()
    messages.error(request,'Certification Cancelled')
    return redirect('inventory:add-job-details',job.id)

def reverse_job(request,job_id):
    job = Job_Certification.objects.get(id=job_id)
    job.status="Pending"
    job.save()
    messages.info(request,'Certification Transaction Reversed')
    return redirect('inventory:add-job-details',job.id)

def approve_job(request,job_id):
    job = Job_Certification.objects.get(id=job_id)
    detail = Job_detail.objects.filter(job_id=job.id,status="Accepted")
    user = request.user
    CertificationInventoryUpdateThread(job,detail,user).start()
    job.status="Approved"
    job.save()
    messages.info(request,'Certification Approved Started')
    return redirect('inventory:add-job-details',job.id)

