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
def accountclass(request):
    
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    accountclass_list = Account_Class.objects.all()
    template = 'accounting/chart-of-account/account-class.html'
    context = {
        'accountclass_list': accountclass_list,
        'heading': 'List of Account Class',
        'pageview': 'Account Class',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_view_chart_of_accounts',raise_exception = True)
def add_accountclass(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    if request.method == 'POST':
        form = AccountClassForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            account_class = Account_Class.objects.get_or_create(name=name.title(),code=code)
            account_classid = Account_Class.objects.get(name=account_class[0])
            messages.info(request,'Account Class Saved')
            return redirect('accounting:add-accountitem',account_classid.id)
    else:
        form =  AccountClassForm()

    template = 'accounting/chart-of-account/create-accountclass.html'
    context = {
        'form':form,
        'heading': 'AccountClass',
        'pageview': 'List of Account Class',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts',raise_exception = True)
def edit_accountclass(request,accountclass_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    accountclass=Account_Class.objects.get(id=accountclass_id)
    if request.method == 'POST':
        form = AccountClassForm(request.POST,instance=accountclass)
        if form.is_valid():
            form.save()
            messages.info(request,'Account Class Updated')
            return redirect('accounting:add-accountitem',accountclass.id)
    else:
        form = AccountClassForm(instance=accountclass)

    template = 'accounting/chart-of-account/create-accountclass.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Currencies',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts',raise_exception = True)
def delete_accountclass(request,accountclass_id):
    accountclass=Account_Class.objects.get(id=accountclass_id)
    accountclass.delete()
    messages.error(request,'Account Class Deleted')
    return redirect('accounting:accountclass-list')


@login_required(login_url='authentication:login')
def uploads_accountclass(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            uploaded_file_url = fs.url(filename)
            import os 

            # Get the complete path to the uploaded file
            file_path = os.path.join(fs.location, filename)
            
            if os.path.exists(file_path):  # Check if the file exists
                empexceldata = pd.read_excel(file_path)
                dbframe = empexceldata
                ChartOfAccountsThread(dbframe).start()
                messages.success(request,'Account Class Data Upload Started')
                return redirect('accounting:accountclass-list')
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
@permission_required('accounting.custom_view_chart_of_accounts',raise_exception = True)
def add_accountitem(request,accountitem_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    accountclass=Account_Class.objects.get(id=accountitem_id)  
    accountitem=AccountItem.objects.filter(account_class_id=accountclass.id) 
    if request.method == 'POST':
        form = AccountItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            currency = AccountItem.objects.get_or_create(name=name.title(),code=code,account_class_id=accountclass)
            messages.info(request,'Account Item Saved')
            return redirect('accounting:add-accountitem',accountclass.id )
    else:
        form =  AccountItemForm()

    template = 'accounting/chart-of-account/add-acountitem.html'
    context = {
        'form':form,
        'heading': 'Account Item',
        'pageview': 'Account Class Details',
        'app_model':app_model,
        'accountclass':accountclass,
        'accountitem':accountitem
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts',raise_exception = True)
def delete_accountitem(request,accountitem_id):
    accountclass=AccountItem.objects.get(id=accountitem_id)
    accountclass_id = accountclass.account_class_id.id
    accountclass.delete()
    messages.error(request,'Account Item Deleted')
    return redirect('accounting:add-accountitem', accountclass_id)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts',raise_exception = True)
def edit_accountitem(request,accountitem_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    item=AccountItem.objects.get(id=accountitem_id)  
    accountclass=Account_Class.objects.get(id=item.account_class_id.id) 
    accountitem=AccountItem.objects.filter(account_class_id=accountclass.id) 
    if request.method == 'POST':
        form = AccountItemForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            messages.info(request,'Account Items Updated')
            return redirect('accounting:add-accountitem',accountclass.id )
    else:
        form =  AccountItemForm(instance=item)

    template = 'accounting/chart-of-account/add-acountitem.html'
    context = {
        'form':form,
        'heading': 'Account Item',
        'pageview': 'Account Class Details',
        'app_model':app_model,
        'accountclass':accountclass,
        'accountitem':accountitem
    }
    return render(request,template,context)



@login_required(login_url='authentication:login')
@permission_required('accounting.custom_view_chart_of_accounts',raise_exception = True)
def add_accountsubitem(request,accountitem_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    accountitem=AccountItem.objects.get(id=accountitem_id)  
    accountsubitem=AccountSubItem.objects.filter(account_item_id=accountitem.id) 
    if request.method == 'POST':
        form = AccountSubItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            accountsubitem = AccountSubItem.objects.get_or_create(name=name.title(),code=code,account_item_id=accountitem)
            messages.info(request,'Account Sub Item Saved')
            return redirect('accounting:add-accountsubitem',accountitem.id )
    else:
        form =  AccountSubItemForm()

    template = 'accounting/chart-of-account/add-accountsubitem.html'
    context = {
        'form':form,
        'heading': 'Account Sub Item',
        'pageview': 'Account Item Details',
        'app_model':app_model,
        'accountsubitem':accountsubitem,
        'accountitem':accountitem
    }
    return render(request,template,context)



@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts',raise_exception = True)
def edit_accountsubitem(request,accountsubitem_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    item=AccountSubItem.objects.get(id=accountsubitem_id)  
    accountitem=AccountItem.objects.get(id=item.account_item_id.id)  
    accountsubitem=AccountSubItem.objects.filter(account_item_id=accountitem.id) 
    if request.method == 'POST':
        form = AccountSubItemForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            messages.info(request,'Account Sub Items Updated')
            return redirect('accounting:add-accountsubitem',accountitem.id  )
    else:
        form =  AccountSubItemForm(instance=item)

    template = 'accounting/chart-of-account/add-accountsubitem.html'
    context = {
        'form':form,
        'heading': 'Account Item',
        'pageview': 'Account Class Details',
        'app_model':app_model,
        'accountsubitem':accountsubitem,
        'accountitem':accountitem
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_view_chart_of_accounts',raise_exception = True)
def add_accountsubsubitem(request,accountsubsubitem_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    accountsubitem=AccountSubItem.objects.get(id=accountsubsubitem_id)  
    accountsubsubitem=AccountLedger.objects.filter(account_sub_item_id=accountsubitem.id) 
    if request.method == 'POST':
        form = AccountSubSubItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            account_number = form.cleaned_data['account_number']
            accountsubsubitem = AccountLedger.objects.get_or_create(name=name.title(),account_number=account_number,account_sub_item_id=accountsubitem)
            messages.info(request,'Account Sub Sub Item Saved')
            return redirect('accounting:add-accountsubsubitem',accountsubitem.id )
    else:
        form =  AccountSubSubItemForm()
    
    template = 'accounting/chart-of-account/add-subsubitem.html'
    context = {
        'form':form,
        'heading': 'Account Sub Sub Item',
        'pageview': 'Account  Sub Item Details',
        'app_model':app_model,
        'accountsubitem':accountsubitem,
        'accountsubsubitem':accountsubsubitem
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_chart_of_accounts',raise_exception = True)
def edit_accountsubsubitem(request,accountsubsubitem_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    item=AccountLedger.objects.get(id=accountsubsubitem_id)  
    accountsubitem=AccountSubItem.objects.get(id=item.account_sub_item_id.id)  
    accountsubsubitem=AccountLedger.objects.filter(account_sub_item_id=accountsubitem.id) 
    if request.method == 'POST':
        form = AccountSubSubItemForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            messages.info(request,'Account Sub Sub Items Updated')
            return redirect('accounting:add-accountsubsubitem',accountsubitem.id  )
    else:
        form =  AccountSubSubItemForm(instance=item)

    template = 'accounting/chart-of-account/add-subsubitem.html'
    context = {
        'form':form,
        'heading': 'Account Sub Sub Item',
        'pageview': 'Account  Sub Item Details',
        'app_model':app_model,
        'accountsubitem':accountsubitem,
        'accountsubsubitem':accountsubsubitem
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_update_chart_of_accounts',raise_exception = True)
def change_subsubitemstatus(request,subsubitem_id):
    subsubitem=AccountLedger.objects.get(id=subsubitem_id)
    accountsubitem=AccountSubItem.objects.get(id=subsubitem.account_sub_item_id.id)
    if subsubitem.status == 'Active':
        subsubitem.status = 'In Active'
        messages.error(request,'Sub  Sub Item De activated')
    else:
        subsubitem.status = 'Active'
        messages.info(request,'Sub  Sub Item Activated')
    subsubitem.save()
    return redirect('accounting:add-accountsubsubitem', accountsubitem.id)

