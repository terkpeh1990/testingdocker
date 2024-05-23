# from msilib.schema import Error
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
from .reader import *
import os 
from inventory.models import Products
from django.db.models import F
from purchase_order.models import *


@login_required(login_url='authentication:login')
@permission_required('dms.custom_create_document',raise_exception = True)
def filemanager(request):
    if request.user.is_superuser:
        category_list = DocumentCategory.objects.all()
        categorygroup = DocumentDestination.objects.all().values('category_id__name').annotate(total=Count('id'),new=Count('is_new'==True))
        latest_files = DocumentDestination.objects.all().order_by('-id')[:10]
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        category_list = DocumentCategory.objects.filter(owner = request.user.id)
        categorygroup = DocumentDestination.objects.filter(staff =request.user.id).values('category_id__name').annotate(total=Count('id'),new=Count('is_new'==True))
        latest_files = DocumentDestination.objects.filter(staff =request.user.id).order_by('-id')[:5]
    
    template = 'dms/filemanager.html'
    context = {
        'category_list': category_list,
        'heading': 'File Manager',
        'pageview': 'File Manager',
        'app_model':app_model,
        'latest_files':latest_files,
        'categorygroup':categorygroup
    }
    return render(request,template,context)

def pin_folder(request,folder_id):
    document = DocumentCategory.objects.get(name=folder_id,owner=request.user)
    document.pin_down = True
    document.save()
    
    messages.success(request,'Folder Pinned')
    return redirect('dms:filemanager-list')

def unpin_folder(request,folder_id):
    document = DocumentCategory.objects.get(name=folder_id,owner=request.user)
    document.pin_down = False
    document.save()
    
    messages.success(request,'Folder Unpinned')
    return redirect('dms:filemanager-list')
        

@login_required(login_url='authentication:login')
@permission_required('dms.custom_create_document',raise_exception = True)
def add_folder(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            folder = DocumentCategory.objects.get_or_create(name=name.title(),owner=request.user,tenant_id=request.user.devision.tenant_id)
            messages.info(request,'Folder Saved')
            return redirect('dms:filemanager-list')
    else:
        form =  FolderForm()

    template = 'dms/create-folder.html'
    context = {
        'form':form,
        'heading': 'Folder',
        'pageview': 'List of Folders',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('dms.custom_create_document',raise_exception = True)
def edit_folder(request,folder_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    document = DocumentCategory.objects.get(owner=request.user,name=folder_id)
        
    if request.method == 'POST':
        form = FolderForm(request.POST,instance=document)
        if form.is_valid():
            form.save()
            messages.info(request,'Folder Updated')
            return redirect('dms:filemanager-list')
    else:
        form =  FolderForm(instance=document)

    template = 'dms/create-folder.html'
    context = {
        'form':form,
        'heading': 'Folder',
        'pageview': 'List of Folders',
        'app_model':app_model
    }
    return render(request,template,context)



@login_required(login_url='authentication:login')
@permission_required('dms.custom_create_document',raise_exception = True)
def add_file(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    users = User.objects.all()
   
    if request.method == 'POST':
        form = FileForm(request.POST,request=request)
        user_to = request.POST.get("user_to")
       
        user_from = request.POST.get("user_from")
    
        if user_from:
            ufrom,_ = user_from.split('-----')
            get_from_user = User.objects.get(staffid=ufrom)
            
        else:
            get_from_user = request.user
        document_from = f"{get_from_user.first_name }  { get_from_user.last_name}"
        document_from_grade = get_from_user.grade.name
        sub_division = get_from_user.sub_division
        if user_to:
            uto,_ = user_to.split('-----')
            get_to_user = User.objects.get(staffid=uto)
            document_to = f"{get_to_user.first_name }  { get_to_user.last_name}"
            document_to_grade = get_from_user.grade.name
        else:
            get_to_user = None
            document_to = None
            document_to_grade = None
        if form.is_valid():
            type_of_document = form.cleaned_data['type_of_document']
            title = form.cleaned_data['title']
            document_date = form.cleaned_data['document_date']
           
            staff_through = form.cleaned_data['staff_through']
            if staff_through:
                document_through = f"{staff_through.first_name }  { staff_through.last_name}"
                document_through_grade = staff_through.grade.name
            else:
                document_through =  None
                document_through_grade =  None


            
            
            document = Document.objects.create(type_of_document=type_of_document,title=title.title(),document_date=document_date,staff_to=get_to_user,document_to=document_to,document_to_grade=document_to_grade,staff_from=get_from_user,document_from=document_from,document_from_grade=document_from_grade,staff_through=staff_through,document_through=document_through,document_through_grade=document_through_grade,sub_division=sub_division,tenant_id=request.user.devision.tenant_id)
            
            try:
                folder = DocumentCategory.objects.get(name="Draft",owner=request.user)
            except DocumentCategory.DoesNotExist:
                folder = DocumentCategory.objects.create(name="Draft",owner=request.user)
            doc = DocumentDestination.objects.create(document_id=document,category_id=folder,staff=document.staff_from,status="Draft")
            by = f"Document Created by {document.document_from } ----  {document.document_from_grade}"
            Documenttimeline.objects.get_or_create(document_id=doc.document_id,timeline_comment = by ,staff= doc.document_id.staff_from)
                
            messages.info(request,'File Save')
            return redirect('dms:add-document_detail', doc.id)
    else:
        form =  FileForm(request=request)

    template = 'dms/create-file.html'
    context = {
        'form':form,
        'heading': 'File',
        'pageview': 'List of Files',
        'app_model':app_model,
        'users':users,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('dms.custom_create_document',raise_exception = True)
def edit_file(request,file_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    users = User.objects.all()
    doc = DocumentDestination.objects.get(id=file_id)
    file = Document.objects.get(id=doc.document_id.id)
        
    if request.method == 'POST':
        user_to = request.POST.get("user_to")
       
        user_from = request.POST.get("user_from")
    
        if user_from:
            ufrom,_ = user_from.split('-----')
            get_from_user = User.objects.get(staffid=ufrom)
        else:
            get_from_user = request.user
        document_from = f"{get_from_user.first_name }  { get_from_user.last_name}"
        document_from_grade = get_from_user.grade.name
        sub_division = get_from_user.sub_division
        if user_to:
            
            uto,_ = user_to.split('-----')
            get_to_user = User.objects.get(staffid=uto)
            document_to = f"{get_to_user.first_name }  { get_to_user.last_name}"
            document_to_grade = get_from_user.grade.name
        else:
            get_to_user = None
            document_to = None
            document_to_grade = None
        form = FileForm(request.POST,instance=file,request=request)
        if form.is_valid():
            
            document=form.save(commit=False)
            document.staff_to=get_to_user
            document.staff_from=get_from_user
            document.document_through =f"{document.staff_through.first_name }  { document.staff_through.last_name}"
            document.document_through_grade = document.staff_through.grade.name
            document.status = False
            document.save()
            messages.info(request,'File Updated')
            return redirect('dms:add-document_detail', doc.id)
    else:
        form =  FileForm(instance=file,request=request)

    template = 'dms/create-file.html'
    context = {
        'form':form,
        'heading': 'File',
        'pageview': 'List of Files',
        'app_model':app_model,
        'doc':doc,
        'users':users,
        
    }
    return render(request,template,context)

def add_document_detail(request,file_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    file = DocumentDestination.objects.get(id=file_id)
    document_detail = DocumentDetails.objects.filter(document_id=file.document_id.id)
    budget = DocumentBudget.objects.filter(document_id=file.document_id.id)
    attachemnt = Documentattachement.objects.filter(document_id=file.document_id.id)
    beneficiary = DocumentBeneficiary.objects.filter(document_id=file.document_id.id)
    product = DocumentProducts.objects.filter(document_id=file.document_id.id)
    if budget:
         cal= budget.aggregate(cc=Sum('amount'))
         total = cal
    else:
        total = 0.00
    
    
    if request.method == 'POST':
        
        form = ParagraphForm(request.POST)
        if form.is_valid():
            paragraph = form.save(commit=False)
            paragraph.document_id = file.document_id
            paragraph.destination = file
            paragraph.save()
            return redirect('dms:add-document_detail',file.id)
    else:
        form =  ParagraphForm()

    template = 'dms/create-paragraph.html'
    context = {
        'form':form,
        'heading': 'File',
        'pageview': 'List of Files',
        'app_model':app_model,
        'file':file,
        'document_detail':document_detail,
        'budget':budget,
        'total':total,
        'attachemnt':attachemnt,
        'beneficiary':beneficiary,
        'product':product
    }
    return render(request,template,context)

def edit_document_detail(request,file_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    document = DocumentDetails.objects.get(id=file_id)
    file = DocumentDestination.objects.get(id=document.destination.id)
    # file = Document.objects.get(id=file_id)
    document_detail = DocumentDetails.objects.filter(document_id=file.document_id.id)
    budget = DocumentBudget.objects.filter(document_id=file.document_id)
    attachemnt = Documentattachement.objects.filter(document_id=file.document_id.id)
    beneficiary = DocumentBeneficiary.objects.filter(document_id=file.document_id.id)
    product = DocumentProducts.objects.filter(document_id=file.document_id.id)
    if budget:
         cal= budget.aggregate(cc=Sum('amount'))
         total = cal
    else:
        total = 0.00
    
    
    if request.method == 'POST':
        
        form = ParagraphForm(request.POST,instance = document)
        if form.is_valid():
            paragraph = form.save(commit=False)
            paragraph.document_id = file.document_id
            paragraph.destination = file
            paragraph.save()

            return redirect('dms:add-document_detail',file.id)
    else:
        form =  ParagraphForm(instance = document)

    template = 'dms/create-paragraph.html'
    context = {
        'form':form,
        'heading': 'File',
        'pageview': 'List of Files',
        'app_model':app_model,
        'file':file,
        'document_detail':document_detail,
        'budget':budget,
        'total':total,
        'beneficiary':beneficiary,
        'product':product
    }
    return render(request,template,context)



def remove_document_item(request,item_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    # file = Document.objects.get(id=file_id)
    
    document_detail = DocumentDetails.objects.get(id=item_id)
    file = DocumentDestination.objects.get(id=document_detail.destination.id)
    # file = Document.objects.get(id=document_detail.document_id.id)
    document_detail.delete()
    messages.error(request,'Paragraph Removed')
    return redirect('dms:add-document_detail',file.id)  

def add_document_currency(request,file_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    doc=DocumentDestination.objects.get(id=file_id)
    file = Document.objects.get(id=doc.document_id.id)
    
    if request.method == 'POST':
        
        form = CurrencyForm(request.POST)
        if form.is_valid():
            file.currency_id =form.cleaned_data['currency_id']
            file.save()
            return redirect('dms:add-document_budget',doc.id)
    else:
        form =  CurrencyForm()

    template = 'dms/create-currency.html'
    context = {
        'form':form,
        'heading': 'Select Budget Currency',
        'pageview': 'Select Budget Currency',
        'app_model':app_model,
        'file':file,
      
    }
    return render(request,template,context)

def edit_document_currency(request,file_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)

    doc=DocumentDestination.objects.get(id=file_id)
    file = Document.objects.get(id=doc.document_id.id)
    
    if request.method == 'POST':
        
        form = CurrencyForm(request.POST,instance=file)
        if form.is_valid():
            file.currency_id =form.cleaned_data['currency_id']
            file.save()
            return redirect('dms:add-document_budget',doc.id)
    else:
        form =  CurrencyForm(instance=file)

    template = 'dms/create-currency.html'
    context = {
        'form':form,
        'heading': 'Select Budget Currency',
        'pageview': 'Select Budget Currency',
        'app_model':app_model,
        'file':file,
      
    }
    return render(request,template,context)

def add_document_budget(request,file_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    doc=DocumentDestination.objects.get(id=file_id)
    file = Document.objects.get(id=doc.document_id.id)
    # budget = DocumentBudget.objects.filter(document_id=file.id)
    budget = DocumentBudget.objects.filter(document_id=file.id)
    if budget:
         cal= budget.aggregate(cc=Sum('amount'))
         total = cal
    else:
        total = 0.00
    if request.method == 'POST':
        
        form = BudgetForm(request.POST, request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            files=form.cleaned_data['file']
            amount=form.cleaned_data['amount']
            DocumentBudget.objects.get_or_create(name=name,attachment=files,amount=amount,document_id=file,destination=doc)
            return redirect('dms:add-document_budget',doc.id)
    else:
        form =  BudgetForm()

    template = 'dms/create-budget.html'
    context = {
        'form':form,
        'heading': 'Budget',
        'pageview': 'Dudget',
        'app_model':app_model,
        'file':file,
        'budget':budget,
        'total':total,
        'doc':doc
    }
    return render(request,template,context)


def remove_budget_item(request,item_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    # file = Document.objects.get(id=file_id)
    budget = DocumentBudget.objects.get(id=item_id)
    doc=DocumentDestination.objects.get(id=budget.destination.id)
    # file = Document.objects.get(id=budget.document_id.id)
    budget.delete()
    messages.error(request,'Budget Removed')
    return redirect('dms:add-document_budget',doc.id)

def view_budget_attachment(request, document_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pdf_document = get_object_or_404(DocumentBudget, pk=document_id)
  
    return render(request, 'dms/view-attachment.html', {'pdf_document':pdf_document,'app_model':app_model})

@login_required(login_url='authentication:login')
@permission_required('dms.custom_create_document',raise_exception = True)
def files(request,folder_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    folder = DocumentCategory.objects.get(name=folder_id,owner=request.user.id)
    category_list = DocumentDestination.objects.filter(staff=request.user.id,category_id=folder.id)
    
    template = 'dms/files.html'
    context = {
        'category_list': category_list,
        'heading': 'Files',
        'pageview': 'File Manager',
        'app_model':app_model,
        'folder':folder,
    }
    return render(request,template,context)


def save_as_draft(request,document_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    # file = Document.objects.get(id=document_id)
    try:
        folder = DocumentCategory.objects.get(name="Draft",owner=request.user)
    except DocumentCategory.DoesNotExist:
        folder = DocumentCategory.objects.create(name="Draft",owner=request.user)
     
        DocumentDestination.objects.get_or_create(id = document_id,category_id=folder,staff=file.staff_from,status="Draft")
    


    messages.success(request,'Saved as Draft')
    return redirect('dms:view_document_detail')

def save_to_send(request,document_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    # file = Document.objects.get(id=document_id)
    try:
        folder = DocumentCategory.objects.get(name="Wait To Send",owner=request.user)
    except DocumentCategory.DoesNotExist:
        folder = DocumentCategory.objects.create(name="Wait To Send",owner=request.user)
    
    doc=DocumentDestination.objects.get(id=document_id)
    
    doc.category_id=folder
    doc.status="Wait To Send"
    doc.save()
    print(doc.id)
    messages.success(request,'Document Saved. Click Send to Send')
    return redirect('dms:view-document_detail',doc.id )

@login_required(login_url='authentication:login')
def add_attachment(request,document_id):
    
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    doc=DocumentDestination.objects.get(id=document_id)
    file = Document.objects.get(id=doc.document_id.id)
    budget = Documentattachement.objects.filter(document_id=file.id)
    if request.method == 'POST':
        form = DocumentUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            files=form.cleaned_data['file']
            Documentattachement.objects.get_or_create(name=name,attachment=files,document_id=file,destination=doc)
            messages.success(request,'File Save')
            return redirect('dms:add-attachment',doc.id)       
    else:
        form = DocumentUploadFileForm()

    template = 'dms/create-attachement.html'
    context = {
        'form': form,
        'budget':budget,
        'file':file,
        'doc':doc
    }
    return render(request, template, context)

def remove_attachemnt(request,item_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    budget = Documentattachement.objects.get(id=item_id)
    doc=DocumentDestination.objects.get(id=budget.destination.id)
    # file = Document.objects.get(id=budget.document_id.id)
    budget.delete()
    messages.error(request,'File Removed')
    return redirect('dms:add-attachment',doc.id)

def view_attachment(request, document_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pdf_document = get_object_or_404(Documentattachement, pk=document_id)
  
    return render(request, 'dms/view-attachment.html', {'pdf_document':pdf_document,'app_model':app_model})



def sendpprove_document(request,document_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    get_document = DocumentDestination.objects.get(id=document_id)

    try:
        inbound = DocumentCategory.objects.get(name="In Bound",owner=get_document.document_id.staff_through)
    except DocumentCategory.DoesNotExist:
        inbound = DocumentCategory.objects.create(name="In Bound",owner=get_document.document_id.staff_through)

    try:
        fromoutbound = DocumentCategory.objects.get(name="Out Bound",owner=request.user)
       
    except DocumentCategory.DoesNotExist:
        fromoutbound = DocumentCategory.objects.create(name="Out Bound",owner=request.user)
        

    try:
        toinbound = DocumentCategory.objects.get(name="In Bound",owner=get_document.document_id.staff_to)
    except DocumentCategory.DoesNotExist:
        toinbound = DocumentCategory.objects.create(name="In Bound",owner=get_document.document_id.staff_to)
    if request.user.has_perm('dms.custom_can_approve_document') and get_document.document_id.staff_through == request.user :
        if get_document.document_id.reverse == True:
                by=f"Document Re approved By {get_document.document_id.document_through } ----  {get_document.document_id.document_through_grade}"
                
                Documenttimeline.objects.create(document_id=get_document.document_id,timeline_comment = by ,staff= get_document.document_id.staff_through)
                get_document.document_id.reverse = False
                get_document.document_id.save()
        else:
            by=f"Document approved by {get_document.document_id.document_through } ----  {get_document.document_id.document_through_grade}"
            Documenttimeline.objects.create(document_id=get_document.document_id,timeline_comment = by ,staff= get_document.document_id.staff_through)
            DocumentDestination.objects.create(document_id=get_document.document_id,category_id=toinbound,staff=get_document.document_id.staff_to,status="Inbound")
        get_document.category_id = fromoutbound
        get_document.status = "Outbound"
        get_document.document_id.status = True
        get_document.document_id.save()
        get_document.save()
        messages.success(request,'Document Sent')
        return redirect('dms:filemanager-list')
    elif request.user.has_perm('dms.custom_can_approve_document') and not get_document.document_id.staff_through:
        DocumentDestination.objects.create(document_id=get_document.document_id,category_id=toinbound,staff=get_document.document_id.staff_to,status="Inbound")
        get_document.category_id = fromoutbound
        get_document.status = "Outbound"
        get_document.document_id.status = True
        get_document.document_id.save()
        get_document.save()
        messages.success(request,'Document Sent')
        return redirect('dms:filemanager-list')
    elif not request.user.has_perm('dms.custom_can_approve_document')  and not get_document.document_id.staff_through:
            messages.error(request,'You do not Have Permission to Send this Memo ')
            return redirect('dms:view-document_detail',get_document.id )

    elif not request.user.has_perm('dms.custom_can_approve_document'):
        if  get_document.document_id.staff_through:
            if get_document.document_id.staff_through.has_perm('dms.custom_can_approve_document'):
                DocumentDestination.objects.create(document_id=get_document.document_id,category_id=inbound,staff=get_document.document_id.staff_through,status="Inbound")
                get_document.category_id = fromoutbound
                get_document.status = "Outbound"
                # get_document.document_id.status = True
                get_document.document_id.save()
                get_document.save()
                get_document.document_id.status = False
                get_document.document_id.save()
                if get_document.document_id.reverse:
                    by=f"Document Corrected By {get_document.document_id.document_from } ----  {get_document.document_id.document_from_grade}"
                    Documenttimeline.objects.create(document_id=get_document.document_id,timeline_comment = by ,staff= get_document.document_id.staff_from)
                    get_document.document_id.reverse = False
                    get_document.document_id.save()

                messages.success(request,'Document Sent')
                return redirect('dms:filemanager-list')
            else:
                messages.error(request,'The Staff Selected Have Permission to Send this Memo')
                return redirect('dms:view-document_detail',get_document.id )
    else:
        return redirect('dms:filemanager-list')


def view_document_detail(request,file_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    doc = DocumentDestination.objects.get(id= file_id)
    file = Document.objects.get(id=doc.document_id.id)
    document_detail = DocumentDetails.objects.filter(document_id=file.id)
    budget = DocumentBudget.objects.filter(document_id=file.id)
    attachemnt = Documentattachement.objects.filter(document_id=file.id)
    beneficiary = DocumentBeneficiary.objects.filter(document_id=file.id)
    minutes = Documenttimeline.objects.filter(document_id=file.id).order_by('-id')
    product = DocumentProducts.objects.filter(document_id=file.id)
    if budget:
         cal= budget.aggregate(cc=Sum('amount'))
         total = cal
    else:
        total = 0.00
    
    
    template = 'dms/view-document.html'
    context = {
       
        'heading': 'File',
        'pageview': 'List of Files',
        'app_model':app_model,
        'file':file,
        'document_detail':document_detail,
        'budget':budget,
        'total':total,
        'attachemnt':attachemnt,
        'minutes':minutes,
        'doc':doc,
        'beneficiary':beneficiary,
        'product':product
    }
    return render(request,template,context)


def add_munites(request,document_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    users = User.objects.all()
    doc = DocumentDestination.objects.get(id= document_id)
    file = Document.objects.get(id=doc.document_id.id)
        
    if request.method == 'POST':
        form = MinuteForm(request.POST)
        user = request.POST.get("user")
        
        if user:
            user,_ =user.split('-----')
            get_from_user = User.objects.get(staffid=user)
        if form.is_valid():
            name = form.cleaned_data['name']
            by=f"Minuted by {request.user.first_name } {request.user.last_name} --- {request.user.grade.name} to {get_from_user.first_name }  {get_from_user.last_name } --- {get_from_user.grade.name}"
            # by = "Minuted by " + " "+ request.user.first_name + " " + request.user.last_name +" to"
            Documenttimeline.objects.create(document_id=file,minutes=name,timeline_comment = by ,staff =get_from_user)
            # document = Document.objects.create(type_of_document=type_of_document,title=title.title(),document_date=document_date,staff_to=get_to_user,staff_from=get_from_user,staff_through=staff_through,tenant_id=request.user.devision.tenant_id)
            try:
                folder = DocumentCategory.objects.get(name="In Bound",owner=get_from_user)
            except DocumentCategory.DoesNotExist:
                folder = DocumentCategory.objects.create(name="In Bound",owner=get_from_user)
            DocumentDestination.objects.create(document_id=file,category_id=folder,staff=get_from_user,status = "Inbound")
            try:
                fo = DocumentCategory.objects.get(name="Out Bound",owner=request.user)
            except DocumentCategory.DoesNotExist:
                fo = DocumentCategory.objects.create(name="Out Bound",owner=request.user)
            doc.category_id = fo
            doc.status = "Outbound"
            doc.save()
            messages.info(request,'File Sent')
            return redirect('dms:filemanager-list')
    else:
        form =  MinuteForm()

    template = 'dms/create-minute.html'
    context = {
        'form':form,
        'heading': 'Minute',
        'pageview': 'Munite',
        'app_model':app_model,
        'users':users,
        'doc':doc
    }
    return render(request,template,context)



def return_document(request,document_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    users = User.objects.all()
    doc = DocumentDestination.objects.get(id= document_id)
    file = Document.objects.get(id=doc.document_id.id)
        
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        
        if form.is_valid():
            type_of_action = form.cleaned_data['type_of_action']
            name = form.cleaned_data['name']

            if type_of_action == 'Return Document For Correction':
                # by = "Returned by" + " "+ request.user.first_name + " " + request.user.last_name +" to"
                
                if file.staff_through and request.user == file.staff_through :
                    try:
                        folder = DocumentCategory.objects.get(name="Returned",owner=file.staff_from)
                    except DocumentCategory.DoesNotExist:
                        folder = DocumentCategory.objects.create(name="Returned",owner=file.staff_from)
                    by=f"Returned by {request.user.first_name } {request.user.last_name} --- {request.user.grade.name} to {file.document_from }  --- {file.document_from_grade}"
                    Documenttimeline.objects.create(document_id=file,minutes=name,timeline_comment = by ,staff = file.staff_from)
                    DocumentDestination.objects.create(document_id=file,category_id=folder,staff=file.staff_from,status = "Returned")

                elif file.staff_through and  not request.user == file.staff_through:
                    try:
                        folder = DocumentCategory.objects.get(name="Returned",owner=file.staff_through)
                    except DocumentCategory.DoesNotExist:
                        folder = DocumentCategory.objects.create(name="Returned",owner=file.staff_through)
                    by=f"Returned by {request.user.first_name } {request.user.last_name} --- {request.user.grade.name} to {file.document_through }  --- {file.document_through_grade}"
                    Documenttimeline.objects.create(document_id=file,minutes=name,timeline_comment = by ,staff = file.staff_through)
                    DocumentDestination.objects.create(document_id=file,category_id=folder,staff=file.staff_through,status = "Returned")
                else:
                    try:
                        folder = DocumentCategory.objects.get(name="Returned",owner=file.staff_from)
                    except DocumentCategory.DoesNotExist:
                        folder = DocumentCategory.objects.create(name="Returned",owner=file.staff_from)
                    by=f"Returned by {request.user.first_name } {request.user.last_name} --- {request.user.grade.name} to {file.document_from }  --- {file.document_from_grade}"
                    Documenttimeline.objects.create(document_id=file,minutes=name,timeline_comment = by ,staff = file.staff_from)
                    DocumentDestination.objects.create(document_id=file,category_id=folder,staff=file.staff_from,status = "Returned")
                    
            
            else:
                
                # by = "Cancelled by" + " "+ request.user.first_name + " " + request.user.last_name +" and returned to"
                if file.staff_through:
                    by=f"Cancelled by {request.user.first_name } {request.user.last_name} --- {request.user.grade.name} and returned to {file.document_through }  --- {file.document_through_grade}"
                    Documenttimeline.objects.create(document_id=file,minutes=name,timeline_comment = by ,staff = file.staff_through)
                    try:
                        folder = DocumentCategory.objects.get(name="Cancelled",owner=file.staff_through)
                    except DocumentCategory.DoesNotExist:
                        folder = DocumentCategory.objects.create(name="Cancelled",owner=file.staff_through)
                    DocumentDestination.objects.create(document_id=file,category_id=folder,staff=file.staff_through,status = "Cancelled")
                else:
                    try:
                        folder = DocumentCategory.objects.get(name="Cancelled",owner=file.staff_from)
                    except DocumentCategory.DoesNotExist:
                        folder = DocumentCategory.objects.create(name="Cancelled",owner=file.staff_from)
                    by=f"Cancelled by {request.user.first_name } {request.user.last_name} --- {request.user.grade.name} and returned to {file.document_from }  --- {file.document_from_grade}"
                    Documenttimeline.objects.create(document_id=file,minutes=name,timeline_comment = by ,staff = file.staff_from)
                    DocumentDestination.objects.create(document_id=file,category_id=folder,staff=file.staff_from,status = "Cancelled")

            
            
            try:
                fo = DocumentCategory.objects.get(name="Out Bound",owner=request.user)
            except DocumentCategory.DoesNotExist:
                fo = DocumentCategory.objects.create(name="Out Bound",owner=request.user)
            doc.category_id = fo
            doc.status = "Outbound"
            doc.save()
            file.reverse = True
            file.save()
            messages.error(request,'File Sent')
            return redirect('dms:filemanager-list')
    else:
        form =  ReturnForm()

    template = 'dms/return_or_cancel.html'
    context = {
        'form':form,
        'heading': 'Return/Cancel Document',
        'pageview': 'Return/Cancel Document',
        'app_model':app_model,
        'doc':doc
    }
    return render(request,template,context)
    
    
    


def add_approved_amount(request,file_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    doc=DocumentDestination.objects.get(id=file_id)
    file = Document.objects.get(id=doc.document_id.id)
    
    if request.method == 'POST':
        
        form = ApprovedBudgetForm(request.POST)
        if form.is_valid():
            file.approved_budget =form.cleaned_data['amount']
            file.save()
            messages.info(request,'Approved Budget Amount Added')
            return redirect('dms:view-document_detail',doc.id)
    else:
        form =  ApprovedBudgetForm()

    template = 'dms/create-amount.html'
    context = {
        'form':form,
        'heading': 'Enter Approved Budget Amount',
        'pageview': 'Enter Approved Budget Amount',
        'app_model':app_model,
        'file':file,
        'doc':doc
      
    }
    return render(request,template,context)




@permission_required('dms.custom_create_document',raise_exception = True)
@login_required(login_url='authentication:login')
def document_beneficiary_upload(request,file_id):
    doc=DocumentDestination.objects.get(id=file_id)
    file = Document.objects.get(id=doc.document_id.id)
    
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
                        phone = '0'+str(i.Contact)
                        DocumentBeneficiary.objects.get_or_create(document_id=file,name=i.Name,phone_number=phone,amount=i.Amount)
                    messages.info(request,'Beneficiary Data Uploaded')
                    return redirect('dms:add-document_detail',doc.id)  
                except IOError:
                    messages.error(request,'Beneficiary Data Upload Error')
                    return redirect('dms:add-document_detail',doc.id)  
            else:
                messages.error(request, 'File not found.')
            return redirect('dms:add-document_detail',doc.id) 
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

@permission_required('dms.custom_can_notify_procurement',raise_exception = True)
@login_required(login_url='authentication:login')
def pull_low_stock_product(request,file_id):
    doc = DocumentDestination.objects.get(id=file_id)
    file = Document.objects.get(id=doc.document_id.id)
    low_stock = Products.objects.filter(tenant_id=request.user.devision.tenant_id.id,inventory__avialable_quantity__lte=F('restock_level'))
    if low_stock:
        for item in low_stock:
            DocumentProducts.objects.get_or_create(document_id = file,product_id=item)
    messages.info(request,'Low Stock Products Pulled')
    return redirect('dms:add-document_detail',doc.id)

