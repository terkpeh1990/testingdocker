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
from dms.models import DocumentDestination,DocumentCategory,Documenttimeline,DocumentDetails,DocumentBudget,Documentattachement,DocumentBeneficiary
from dms.forms import DocumentUploadFileForm
from  .utils import *
from .sms_thread import *
from django.shortcuts import get_object_or_404
import inflect
import os 

 

@login_required(login_url='authentication:login')
# @permission_required('accounting.custom_create_pv')
def manage_paymentvouchers(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pv_list = PaymentVoucher.objects.filter(sub_division=request.user.sub_division.id)
    template = 'accounting/pv/pv_list.html'
    context = {
        'pv_list': pv_list,
        'heading': 'List of Payment Vouchers',
        'pageview': 'Payment Vouchers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_authorise_annd_pass_pv')
def ia_paymentvouchers(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    pv_list = Pveligibility.objects.filter(sub_division=request.user.sub_division.id)
    
    template = 'accounting/pv/ia_list.html'
    context = {
        'pv_list': pv_list,
        'heading': 'List of Payment Vouchers',
        'pageview': 'Payment Vouchers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_authorise_pv',raise_exception = True)
def pending_paymentvouchers(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pv_list = PaymentVoucher.objects.filter(sub_division=request.user.sub_division.id,status='Pending',notify=True)
    template = 'accounting/pv/pv_list.html'
    context = {
        'pv_list': pv_list,
        'heading': 'List of Payment Vouchers',
        'pageview': 'Payment Vouchers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_approve_pv',raise_exception = True)
def approve_paymentvouchers(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pv_list = PaymentVoucher.objects.filter(sub_division=request.user.sub_division.id,status='Authorised')
    template = 'accounting/pv/pv_list.html'
    context = {
        'pv_list': pv_list,
        'heading': 'List of Payment Vouchers',
        'pageview': 'Payment Vouchers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_authorise_annd_pass_pv',raise_exception = True)
def authorisedpassed_paymentvouchers(request):
    account_unit = ['Accounts','ACCOUNTS','Account']
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.user.has_perm('accounting.custom_headoffice'):
        pv_list = PaymentVoucher.objects.filter(sub_division__name__in=account_unit,status='Approved')
    else:
        pv_list = PaymentVoucher.objects.filter(sub_division=request.user.sub_division.id,status='Approved')
    template = 'accounting/pv/pv_list.html'
    context = {
        'pv_list': pv_list,
        'heading': 'List of Payment Vouchers',
        'pageview': 'Payment Vouchers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_add_cheque_no',raise_exception = True)
def checknumber_paymentvouchers(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pv_list = PaymentVoucher.objects.filter(sub_division=request.user.sub_division.id,status='Authorised & Passed')
    template = 'accounting/pv/pv_list.html'
    context = {
        'pv_list': pv_list,
        'heading': 'List of Payment Vouchers',
        'pageview': 'Payment Vouchers',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_pay_pv',raise_exception = True)
def payables(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    pv_list = Payables.objects.filter(sub_division=request.user.sub_division.id)
    
    template = 'accounting/pv/payables.html'
    context = {
        'pv_list': pv_list,
        'heading': 'List of Payables',
        'pageview': 'Payment Vouchers',
        'app_model':app_model,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
# @permission_required('accounting.custom_add_cheque_no')
def all_paymentvouchers(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.user.has_perm('accounting.custom_headoffice'):
        pv_list = PaymentVoucher.objects.all()
    elif request.user.has_perm('accounting.custom_regional'):
        pv_list = PaymentVoucher.objects.filter(sub_division__devision=request.user.sub_division.devision.id)
    else:
        pv_list = PaymentVoucher.objects.filter(sub_division=request.user.sub_division.id)

    template = 'accounting/pv/pv_list.html'
    context = {
        'pv_list': pv_list,
        'heading': 'List of Payment Vouchers',
        'pageview': 'Payment Vouchers',
        'app_model':app_model
    }
    return render(request,template,context)



@login_required(login_url='authentication:login')
@permission_required('dms.custom_can_create_pv_from_document')
def add_pv(request,document_id):
   
    doc = DocumentDestination.objects.get(id=document_id)
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    check_year = check_active_accounting_year()
    if check_year == 'NO ACCOUNT' or check_year == 'CLOSE':
        messages.error(request,'Please make sure Fiscal year is Active')
        return redirect('dms:view-document_detail',doc.id)

    else:
        ff = Fiscal_year.objects.all().order_by('id').last()
        if request.method == 'POST':
            form = PvForm(request.POST,request=request)
            if form.is_valid():
                type_of_pay = form.cleaned_data['type_of_pay']
                pv = form.save(commit=False)
                if type_of_pay == 'Third Party':
                    pv.payto = f"{doc.document_id.supplier.name}" 
                    pv.pay_to_address = f"{doc.document_id.supplier.address},{doc.document_id.supplier.city},{doc.document_id.supplier.country}"  
                elif type_of_pay == 'Refund':
                    pv.payto = f"{doc.document_id.staff_from.last_name} {doc.document_id.staff_from.first_name}" 
                    pv.pay_to_address = "P.O.BOX M96, Ministries-Accra, Ghana"
                else:
                    pv.payto = "Auditor General Ghana Audit Service" 
                    pv.pay_to_address = "P.O.BOX M96, Ministries-Accra, Ghana"
                pv.document = doc.document_id
                pv.document_destination = doc
                pv.description =doc.document_id.title
                pv.devision = request.user.devision
                pv.sub_division = request.user.sub_division
                pv.prepared_by = request.user
                pv.acoounting_year = ff
                pv.save()
                by=f"Prepared By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
                Pvtimeline.objects.get_or_create(pv_id=pv,timeline_comment=by,staff=request.user)
                dby = f"PV Generated by {request.user.first_name } { request.user.last_name} ---- {request.user.grade}"
                Documenttimeline.objects.get_or_create(document_id=doc.document_id,timeline_comment = dby ,staff= request.user)
                messages.info(request,'Pv Initiated')
                return redirect('accounting:add-deatil-pv',pv.id)
        else:
            form = PvForm(request=request)

    template = 'accounting/pv/create-pv.html'
    context = {
        'form':form,
        'heading': 'Payment Voucher',
        'pageview': 'List of Payment Voucher',
        'app_model':app_model
    }
    return render(request,template,context)

login_required(login_url='authentication:login')
@permission_required('dms.custom_can_create_pv_from_document')
def add_pv_without_doc(request):
    
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    check_year = check_active_accounting_year()
    if check_year == 'NO ACCOUNT' or check_year == 'CLOSE':
        messages.error(request,'Please make sure Fiscal year is Active')
        return redirect('accounting:paymentvoucher-list')

    else:
        ff = Fiscal_year.objects.all().order_by('id').last()
        if request.method == 'POST':
            form = NoDocPvForm(request.POST,request=request)
            if form.is_valid():
                pv = form.save(commit=False)
                pv.devision = request.user.devision
                pv.sub_division = request.user.sub_division
                pv.prepared_by = request.user
                pv.acoounting_year = ff
                pv.save()
                by=f"Prepared By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
                Pvtimeline.objects.get_or_create(pv_id=pv,timeline_comment=by,staff=request.user)
                messages.info(request,'Pv Initiated')
                return redirect('accounting:add-deatil-pv',pv.id)
        else:
            form = NoDocPvForm(request=request)

    template = 'accounting/pv/nodocpv.html'
    context = {
        'form':form,
        'heading': 'Payment Voucher',
        'pageview': 'List of Payment Voucher',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_create_pv')
def update_pv(request,pv_id):
    pvs = PaymentVoucher.objects.get(id=pv_id)
    if pvs.document:
        doc = Document.objects.get(id=pvs.document.id)
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        if pvs.document:
            form = PvForm(request.POST,instance=pvs,request=request)
        else:
            form = NoDocPvForm(request.POST,instance=pvs,request=request)
        if form.is_valid():
            type_of_pay = form.cleaned_data['type_of_pay']
            pv = form.save(commit=False)
            if pvs.document:
                
                if type_of_pay == 'Third Party':
                    pv.payto = f"{doc.supplier.name}" 
                    pv.pay_to_address = f"{doc.supplier.address},{doc.supplier.city},{doc.supplier.country}"  
                elif type_of_pay == 'Refund':
                    pv.payto = f"{doc.staff_from.last_name} {doc.staff_from.first_name}" 
                    pv.pay_to_address = "P.O.BOX M96, Ministries-Accra, Ghana"
                else:
                    pv.payto = "Auditor General Ghana Audit Service" 
                    pv.pay_to_address = "P.O.BOX M96, Ministries-Accra, Ghana"
                
                pv.document = doc
                pv.description =doc.title
                dby = f"PV Updated by {request.user.first_name } { request.user.last_name} ---- {request.user.grade}"
                Documenttimeline.objects.get_or_create(document_id=doc,timeline_comment = dby ,staff= request.user)
            
            pv.devision = request.user.devision
            pv.sub_division = request.user.sub_division
            pv.prepared_by = request.user
            pv.acoounting_year = pvs.acoounting_year
            pv.save()
            by=f"Updated By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
            Pvtimeline.objects.get_or_create(pv_id=pv,timeline_comment=by,staff=request.user)
            messages.info(request,'Pv Updated')
            return redirect('accounting:add-deatil-pv',pvs.id)
    else:
        if pvs.document:
            form = PvForm(instance=pvs,request=request)
        else:
            form = NoDocPvForm(instance=pvs,request=request)
        
    if pvs.document:
        template = 'accounting/pv/create-pv.html'
    else:
        template = 'accounting/pv/nodocpv.html'

    context = {
        'form':form,
        'heading': 'Payment Voucher',
        'pageview': 'List of Payment Voucher',
        'app_model':app_model
    }
    return render(request,template,context)



@login_required(login_url='authentication:login')
@permission_required('dms.custom_can_create_pv_from_document',raise_exception = True)
def add_pv_detail(request,pv_id):
   
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    accounts = AccountLedger.objects.filter(status="Active")
    pv = PaymentVoucher.objects.get(id=pv_id)
    detail =PvDetail.objects.filter(pv_id=pv.id)
    beneficiary = PaymentVoucherBeneficiary.objects.filter(pv_id=pv.id)
    attachemnt =Paymentattachement.objects.filter(pv_id=pv.id)
    cheque =PvPayment.objects.filter(pv_id=pv.id)
    
    p = inflect.engine()
    if detail:
        cal= detail.aggregate(cc=Sum('amount'))
        if pv.withholding_tax_amount is None :
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            amount_in_words=p.number_to_words(total)
        elif pv.withholding_tax_amount > 0.00:
            precentage = pv.withholding_tax_amount/100
            sub_total = cal['cc']
            tax = cal['cc']*precentage
            total = cal['cc']-tax
            amount_in_words=p.number_to_words(total)
        else:
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            amount_in_words=p.number_to_words(total)
    else:
        total = 0.00
        sub_total = 0.00
        tax = 0.00
        amount_in_words=p.number_to_words(total)
   
    if request.method == 'POST':
        form = PvDetailForm(request.POST)
        coa = request.POST.get("coa")
       
        if coa:
            c,_ = coa.split('-----')
            get_coa = AccountLedger.objects.get(account_number=c)
       
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            pvd = PvDetail.objects.get_or_create(pv_id=pv,accout_code=get_coa,description=description,amount=amount)
            messages.info(request,'Payment Voucher Item Added')
            return redirect('accounting:add-deatil-pv',pv.id)
    else:
        form =  PvDetailForm()

    template = 'accounting/pv/create-pvdetail.html'
    context = {
        'form':form,
        'tax':tax,
        'total':total,
        'heading': 'Payment Voucher',
        'pageview': 'List of Payment Voucher',
        'app_model':app_model,
        'accounts':accounts,
        'pv':pv,
        'detail':detail,
        'sub_total':sub_total,
        'attachemnt':attachemnt,
        'amount_in_words':amount_in_words,
        'beneficiary':beneficiary,
        'cheque':cheque,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('dms.custom_can_create_pv_from_document',raise_exception = True)
def delete_pvitem(request,pvitem_id):
    item=PvDetail.objects.get(id=pvitem_id)
    pvid = item.pv_id
    item.delete()
    messages.error(request,'Item Removed')
    return redirect('accounting:add-deatil-pv',pvid)

@login_required(login_url='authentication:login')
# @permission_required('accounting.custom_authorise_annd_pass_pv',raise_exception = True)
def pv_detail(request,pv_id):
   
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    accounts = AccountLedger.objects.filter(status="Active")
    pv = PaymentVoucher.objects.get(id=pv_id)
    minutes=Pvtimeline.objects.filter(pv_id = pv.id).order_by('-id')
    detail =PvDetail.objects.filter(pv_id=pv.id)
    attachemnt =Paymentattachement.objects.filter(pv_id=pv.id)
    beneficiary = PaymentVoucherBeneficiary.objects.filter(pv_id=pv.id)
    cheque =PvPayment.objects.filter(pv_id=pv.id)
    p = inflect.engine()
    if detail:
        cal= detail.aggregate(cc=Sum('amount'))
        if pv.withholding_tax_amount is None :
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            amount_in_words=p.number_to_words(total)
        elif pv.withholding_tax_amount > 0.00:
            precentage = pv.withholding_tax_amount/100
            sub_total = cal['cc']
            tax = cal['cc']*precentage
            total = cal['cc']-tax
            amount_in_words=p.number_to_words(total)
        else:
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            amount_in_words=p.number_to_words(total)
    else:
        total = 0.00
        sub_total = 0.00
        tax = 0.00
        amount_in_words=p.number_to_words(total)
   
    template = 'accounting/pv/view_pv.html'
    context = {
        
        'tax':tax,
        'total':total,
        'heading': 'Payment Voucher',
        'pageview': 'List of Payment Voucher',
        'app_model':app_model,
        'accounts':accounts,
        'pv':pv,
        'detail':detail,
        'sub_total':sub_total,
        'minutes':minutes,
        'attachemnt':attachemnt,
        'amount_in_words':amount_in_words,
        'beneficiary':beneficiary,
        'cheque':cheque,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
# @permission_required('dms.custom_can_create_pv_from_document',raise_exception = True)
def change_pv_status(request,pv_id):
    item=PaymentVoucher.objects.get(id=pv_id)
    ben = PaymentVoucherBeneficiary.objects.filter(pv_id=item)
    detail =PvDetail.objects.filter(pv_id=item.id)
    if detail:
        cal= detail.aggregate(cc=Sum('amount'))
        if item.withholding_tax_amount is None :
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            # amount_in_words=p.number_to_words(total)
        elif item.withholding_tax_amount > 0.00:
            precentage = item.withholding_tax_amount/100
            sub_total = cal['cc']
            tax = cal['cc']*precentage
            total = cal['cc']-tax
            # amount_in_words=p.number_to_words(total)
        else:
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            # amount_in_words=p.number_to_words(total)
    else:
        total = 0.00
        sub_total = 0.00
        tax = 0.00
    
        amount_in_words=p.number_to_words(total)
    if request.user.has_perm('dms.custom_can_create_pv_from_document') and item.status == 'Pending':
        if not ben:
            messages.error(request,'Payment Voucher Cannot be sent for Authorization without beneficiary')
        else:
            item.notify = True
            messages.info(request,'Payment Voucher Sent for Authorization')
            NotificationThread(item).start()
        if item.document_destination:
            try:
                folder = DocumentCategory.objects.get(name="PV Generated",owner=request.user)
            except DocumentCategory.DoesNotExist:
                folder = DocumentCategory.objects.create(name="PV Generated",owner=request.user)
            item.document_destination.category_id = folder
            item.document_destination.status = 'Pv Created'
            item.document_destination.save()
        item.save()

    elif request.user.has_perm('accounting.custom_authorise_pv') and item.status == 'Pending':
        item.status = 'Authorised'
        by=f"Recommended For Approval By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,staff=request.user)
        item.authorized_by = request.user
        messages.info(request,'Payment Voucher Sent for Approval')
        item.save()
        dby = f"Pv Recommended For Approval By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        if item.document:
            Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)
        NotificationThread(item).start()

    elif request.user.has_perm('accounting.custom_approve_pv') and item.status == 'Authorised':
        item.status = 'Approved'
        by=f"Approved By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,staff=request.user)
        if item.document:
            dby = f"Pv Approved By {request.user.first_name} {request.user.last_name} ---- {request.user.grade} And Sent To Internal Audit"
            Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)
        item.approved_by = request.user
        messages.info(request,'Payment Voucher Approved and Sent to Internal Audit')
        item.save()
        AuditNotificationThread(item).start()
    else:
        pass
    
    item.pv_amount = total
    item.save()
    
    return redirect('accounting:pv-detail',item.id)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_add_cheque_no',raise_exception = True)
def add_cheque_no(request,pv_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    check_year = check_active_accounting_year()
    if check_year == 'NO ACCOUNT' or check_year == 'CLOSE':
        messages.error(request,'Please make sure Fiscal year is Active')
        return redirect('accounting:paymentvoucher-list')

    else:
        item=PaymentVoucher.objects.get(id=pv_id)
        if request.method == 'POST':
            
            form = ChequeForm(request.POST)
            if form.is_valid():
                cheque = form.cleaned_data['cheque_number']
                check_date = form.cleaned_data['cheque_number_date']
                amount = form.cleaned_data['amount']
                type_of_payment = form.cleaned_data['type_of_payment']
                pv_number = form.cleaned_data['pv_number']
                if type_of_payment == 'Others':
                    child_pv = PaymentVoucher.objects.get(id=pv_number)
                else:
                    child_pv = item
                cheque,created = PvPayment.objects.get_or_create(cheque_number_date=check_date,type_of_payment=type_of_payment,pv_id=item,childpv_id=child_pv,cheque_number=cheque,amount=amount)
                
               
                # item.cheque_number_date =check_date
                # item.cheque_number =cheque
                by=f"Cheque Number Entered By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
                Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,staff=request.user)
                if item.document:
                    dby = f"Pv Cheque Ready and Cheque no Entered By {request.user.first_name} {request.user.last_name} ---- {request.user.grade} and Yet To Be Recieved By Cashier"
                    Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)    
                Payables.objects.get_or_create(pv_id = item, amount=item.pv_amount,devision= item.devision,sub_division=item.sub_division,acoounting_year=item.acoounting_year)
                messages.info(request,'Cheque Number Entered')
                return redirect('accounting:pv-detail',item.id)
        else:
            form =  ChequeForm()

    template = 'accounting/pv/cheque_number.html'
    context = {
        'form':form,
        'heading': 'Enter Cheque Number',
        'pageview': 'Enter Cheque Number',
        'app_model':app_model,
        'item':item
      
    }
    return render(request,template,context)




@login_required(login_url='authentication:login')
@permission_required('dms.custom_can_create_pv_from_document',raise_exception = True)
def add_pv_attachment(request,pv_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pv=PaymentVoucher.objects.get(id=pv_id)
    attachment = Paymentattachement.objects.filter(pv_id=pv.id)
    if request.method == 'POST':
        form = DocumentUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            files=form.cleaned_data['file']
            Paymentattachement.objects.get_or_create(name=name,attachment=files,pv_id=pv)
            messages.success(request,'File Save')
            return redirect('accounting:add-pv-attachment',pv.id)       
    else:
        form = DocumentUploadFileForm()

    template = 'accounting/pv/create-attachment.html'
    context = {
        'form': form,
        'attachment':attachment,
        'pv':pv
    }
    return render(request, template, context)

def remove_pvattachemnt(request,item_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    attachemtnt = Paymentattachement.objects.get(id=item_id)
    pv=PaymentVoucher.objects.get(id=attachemtnt.pv_id.id)
    attachemtnt.delete()
    messages.error(request,'File Removed')
    return redirect('accounting:add-pv-attachment',pv.id)

def sendbackto_ia_pvattachemnt(request,pv_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
   
    item=PaymentVoucher.objects.get(id=pv_id)
    item.status = 'Approved'
    item.save()
    by=f"Pv Corrected By {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
    Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,staff=request.user)
    if item.document:
        dby = f"Pv Corrected  By {request.user.first_name} {request.user.last_name} ---- {request.user.grade} and sent back to Internal Audit"
        Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)
    AuditNotificationThread(item).start()
    messages.info(request,'Pv Sent Back to Internal Audit')
    return redirect('accounting:pv-detail',item.id)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_authorise_annd_pass_pv',raise_exception = True)
def check_pv_eligibility(request,pv_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    item=PaymentVoucher.objects.get(id=pv_id)
    detail =PvDetail.objects.filter(pv_id=item.id)
    p = inflect.engine()
    if detail:
        cal= detail.aggregate(cc=Sum('amount'))
        if item.withholding_tax_amount is None :
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            amount_in_words=p.number_to_words(total)
        elif item.withholding_tax_amount > 0.00:
            precentage = item.withholding_tax_amount/100
            sub_total = cal['cc']
            tax = cal['cc']*precentage
            total = cal['cc']-tax
            amount_in_words=p.number_to_words(total)
        else:
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            amount_in_words=p.number_to_words(total)
    else:
        total = 0.00
        sub_total = 0.00
        tax = 0.00
        amount_in_words=p.number_to_words(total)

    try:
        ia = Pveligibility.objects.get(pv_id= item.id)
    except Pveligibility.DoesNotExist:
        ia = None
    
    if request.method == 'POST':
        if ia is not None:
            form = InternalAuditForm(request.POST,instance = ia)
        else: 
            form = InternalAuditForm(request.POST)


        if form.is_valid():
            new_ia= form.save(commit=False)
            new_ia.pv_id =item
            new_ia.type_of_pv =item.type_of_pv
            new_ia.withholding_tax = item.withholding_tax
            new_ia.withholding_tax_amount = tax
            new_ia.gross_amount = sub_total
            new_ia.bankaccounttype = item.bankaccounttype
            new_ia.devision = request.user.devision
            new_ia.sub_division = request.user.sub_division
            new_ia.save()
            print(new_ia.status)
            if new_ia.status == 'Completed':
                item.status = "Authorised & Passed"
                by=f"Pv Eligibility Check Completed  By  {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
                Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,staff=request.user)
                item.authorized_and_passed_by = request.user
                item.save()
                NotificationThread(item).start()
                dby = f"Pv Eligibility Test Passed By {request.user.first_name} {request.user.last_name} ---- {request.user.grade} and Returned to Accounts For Payment Proccess"
                Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)
            elif new_ia.status == 'Returned':
                item.status = "Returned"
                item.save()
                by=f"Pv Eligibility Check Failed  By  {request.user.first_name} {request.user.last_name} ---- {request.user.grade} and Returned to accounts for update or correction"
                Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,minutes=new_ia.remarks,staff=request.user)
                NotificationThread(item).start()
                dby = f"Pv Eligibility Test Failed By {request.user.first_name} {request.user.last_name} ---- {request.user.grade} and Returned to Accounts For update or correction"
                Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby,minutes=new_ia.remarks ,staff= request.user)
            else:
                item.status = "Cancelled"
                item.save()
                by=f"Pv Cancelled  By  {request.user.first_name} {request.user.last_name} ---- {request.user.grade} and Returned to accounts"
                Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,minutes=new_ia.remarks,staff=request.user)
                NotificationThread(item).start()
                dby = f"Pv Cancelled {request.user.first_name} {request.user.last_name} ---- {request.user.grade} and Returned to Accounts For update or correction"
                Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby,minutes=new_ia.remarks,staff= request.user)

            
            
            messages.info(request,'Pv Eligibity Checked')
            return redirect('accounting:ia-detail',new_ia.id)
    else:
        if ia is not None:
            form =  InternalAuditForm(instance = ia)
        else:
            form =  InternalAuditForm()

    template = 'accounting/pv/pv_elegibility.html'
    context = {
        'form':form,
        'heading': 'Pv Elegibility Check',
        'pageview': 'Pv Elegibility Check',
        'app_model':app_model,
        'item':item,
        'amount_in_words':amount_in_words
      
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
# @permission_required('accounting:custom_view_pv',raise_exception = True)
def ia_detail(request,ia_id):
   
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    ia = Pveligibility.objects.get(id=ia_id)
    pv = PaymentVoucher.objects.get(id=ia.pv_id)
    minutes=Pvtimeline.objects.filter(pv_id = pv.id).order_by('-id')
    detail =PvDetail.objects.filter(pv_id=pv.id)
    attachemnt =Paymentattachement.objects.filter(pv_id=pv.id)
    beneficiary = PaymentVoucherBeneficiary.objects.filter(pv_id=pv.id)
    p = inflect.engine()
    if detail:
        cal= detail.aggregate(cc=Sum('amount'))
        if pv.withholding_tax_amount is None :
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            amount_in_words=p.number_to_words(total)
        elif pv.withholding_tax_amount > 0.00:
            precentage = pv.withholding_tax_amount/100
            sub_total = cal['cc']
            tax = cal['cc']*precentage
            total = cal['cc']-tax
            amount_in_words=p.number_to_words(total)
        else:
            tax = 0.00
            sub_total = cal['cc']
            total = cal['cc']
            amount_in_words=p.number_to_words(total)
    else:
        total = 0.00
        sub_total = 0.00
        tax = 0.00
        amount_in_words=p.number_to_words(total)
   
    template = 'accounting/pv/ia-detail.html'
    context = {
        
        'tax':tax,
        'total':total,
        'heading': 'Payment Voucher',
        'pageview': 'List of Payment Voucher',
        'app_model':app_model,
        'pv':pv,
        'detail':detail,
        'sub_total':sub_total,
        'minutes':minutes,
        'attachemnt':attachemnt,
        'ia':ia,
        'amount_in_words':amount_in_words,
        'beneficiary':beneficiary
    }
    return render(request,template,context)

def view_pvattachment(request, attachemnt_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pdf_document = get_object_or_404(Paymentattachement, pk=attachemnt_id)
    return render(request, 'accounting/pv/view-attachment.html', {'pdf_document':pdf_document,'app_model':app_model})


def view_pvdocument_detail(request,pv_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pv = PaymentVoucher.objects.get(id=pv_id)
    file = Document.objects.get(id=pv.document.id)
    document_detail = DocumentDetails.objects.filter(document_id=file.id)
    budget = DocumentBudget.objects.filter(document_id=file.id)
    attachemnt = Documentattachement.objects.filter(document_id=file.id)
    minutes = Documenttimeline.objects.filter(document_id=file.id).order_by('-id')
    # ia=Pveligibility.objects.get(pv_id=pv.id)
    if budget:
         cal= budget.aggregate(cc=Sum('total'))
         total = cal
    else:
        total = 0.00
    
    
    template = 'accounting/pv/pv-document.html'
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
        'pv':pv,
        # 'ia':ia
    }
    return render(request,template,context)


def view_pvdocattachment(request, pv_id,attachment_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pv = PaymentVoucher.objects.get(id=pv_id)
    pdf_document = get_object_or_404(Documentattachement, pk=attachment_id)
    return render(request, 'accounting/pv/pv_doc_attachment.html', {'pdf_document':pdf_document,'app_model':app_model,'pv':pv})


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_pay_pv',raise_exception = True)
def notifypayee(request,pv_id):
    item=PaymentVoucher.objects.get(id=pv_id)
    ap=Payables.objects.get(pv_id = item.id)
    beneficiary =PaymentVoucherBeneficiary.objects.filter(pv_id=item.id)
    ap.status ='Recipient Notified'
    ap.save()
    by=f"Pv Funds Ready and Payee have been notified by  {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
    Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,staff=request.user)
    item.status = 'Payee Notified'
    item.save()
    if item.document and beneficiary:
        dby = f"Pv Funds Ready and Payee have been notified by {request.user.first_name} {request.user.last_name} ---- {request.user.grade} "
        Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)
        IndividualNotification(item).start()
    elif item.document and beneficiary is None:
        dby = f"Pv Funds Ready and Payee have been notified by {request.user.first_name} {request.user.last_name} ---- {request.user.grade} "
        Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)
        code = random_with_N_digits(6)
        ap.code = code
        ap.save()
        PayeeNotificationThread(item,code).start()
    elif not item.document and beneficiary:
        IndividualNotification(item).start()
    else:
        pass

    messages.info(request,'Notification Done')
    return redirect('accounting:pv-detail',item.id)

@login_required(login_url='authentication:login')
@permission_required('accounting.custom_add_cheque_no',raise_exception = True)
def comfirm_checknumber(request,pv_id):
    item=PaymentVoucher.objects.get(id=pv_id)
    item.status = 'Check No Entered'
    item.save()
    NotificationThread(item).start()
    messages.info(request,'Cheque Number Comfirm')
    return redirect('accounting:pv-detail',item.id)

@login_required(login_url='authentication:login')
@permission_required('dms.custom_can_create_pv_from_document',raise_exception = True)
def pull_beneficiaries(request,pv_id):
    item=PaymentVoucher.objects.get(id=pv_id)
    document = Document.objects.get(id=item.document.id)
    beneficiary = DocumentBeneficiary.objects.filter(document_id=document.id)

    if beneficiary:
        for i in beneficiary:
            PaymentVoucherBeneficiary.objects.get_or_create(pv_id=item,name=i.name,phone_number=i.phone_number,amount=i.amount,ref=document.id)
    elif document.approved_budget > 1.00 and not beneficiary:
        name =f"{document.staff_from.last_name } {document.staff_from.first_name}"
        phone_number = f"{document.staff_from.phone_number}"
        PaymentVoucherBeneficiary.objects.get_or_create(pv_id=item,name=name,phone_number=phone_number,amount=document.approved_budget,ref=document.id)
    else:
        pass

    messages.info(request,'Beneficiaries Extracted Successfully')
    return redirect('accounting:add-deatil-pv',item.id)

# @login_required(login_url='authentication:login')
# @permission_required('accounting.custom_authorise_annd_pass_pv',raise_exception = True)
# def paypv(request,pv_id):
#     item=PaymentVoucher.objects.get(id=pv_id)
#     ap=Payables.objects.get(pv_id = item.id)
#     by=f"Pv Funds Ready and Payee have been notified by  {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
#     Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,staff=request.user)
#     item.status = 'Payee Notified'
#     item.save()
#     ap.status ='Recipient Notified'
#     ap.save()
#     if item.document:
#         dby = f"Pv Funds Ready and Payee have been notified by {request.user.first_name} {request.user.last_name} ---- {request.user.grade} "
#         Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)
#         PayeeNotificationThread(item).start()
#     messages.error(request,'Item Removed')
#     return redirect('accounting:add-deatil-pv',pvid)

@permission_required('dms.custom_create_document',raise_exception = True)
@login_required(login_url='authentication:login')
def pv_beneficiary_upload(request,pv_id):
    pv = PaymentVoucher.objects.get(id=pv_id)
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
                        
                        PaymentVoucherBeneficiary.objects.get_or_create(pv_id=pv,name=i.Name,phone_number=i.Contact,amount=i.Amount)
                        
                    messages.info(request,'Beneficiary Data Uploaded')
                    return redirect('accounting:add-deatil-pv',pv.id)  
                except IOError:
                    messages.error(request,'Beneficiary Data Upload Error')
                    return redirect('accounting:add-deatil-pv',pv.id)  
            else:
                messages.error(request, 'File not found.')
            return redirect('accounting:add-deatil-pv',pv.id) 
    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_pay_pv',raise_exception = True)
def list_pv_beneficiary(request,pv_id):
   
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    pv = PaymentVoucher.objects.get(id=pv_id)
    beneficiary = PaymentVoucherBeneficiary.objects.filter(pv_id=pv.id)
    payable = Payables.objects.get(pv_id = pv.id)
    p = inflect.engine()
    if beneficiary:
        total= beneficiary.aggregate(cc=Sum('amount'))
        amount_received= beneficiary.aggregate(cc=Sum('amount_received'))
        balance = beneficiary.aggregate(cc=Sum('balance'))

        totals= total['cc']
        amount_receiveds = amount_received['cc']
        balances = balance['cc']


    
    else:
        totals = 0.00
        amount_receiveds = 0.00
        balances = 0.00

    if balances <= 0.00:
        
        pv.status = 'Paid'
        pv.save()
        payable.status = 'Amount Paid'
        payable.save()
        by=f"All Funds paid by  {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        Pvtimeline.objects.get_or_create(pv_id=pv,timeline_comment=by,staff=request.user)

        if pv.document:
            dby = f"All Funds Paid by {request.user.first_name} {request.user.last_name} ---- {request.user.grade} "
            Documenttimeline.objects.get_or_create(document_id=pv.document,timeline_comment = dby ,staff= request.user)
         
   
    template = 'accounting/pv/beneficiary.html'
    context = {
        
        
        'heading': 'Payment Voucher',
        'pageview': 'List of Payment Voucher',
        'app_model':app_model,
        'pv':pv,
        'totals':totals,
        'amount_receiveds':amount_receiveds,
        'balances':balances,
        'beneficiary':beneficiary


        
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('accounting.custom_pay_pv',raise_exception = True)
def comfirm_code(request,item_id):
   
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    # pv = PaymentVoucher.objects.get(id=pv_id)
    beneficiary = PaymentVoucherBeneficiary.objects.get(id=item_id)
    if request.method == 'POST':
        form = ComfirmForm(request.POST, instance=beneficiary)
        if form.is_valid():
            form.save()
            messages.info(request,'Code Confirmed')
            return redirect('accounting:comfirm-code',beneficiary.id)  

    else:
        form =ComfirmForm(instance=beneficiary)

    template = 'accounting/pv/comfirm.html'
    context = {
        
        
        'heading': 'Payment Voucher Payment Confirmation',
        'pageview': 'List of Payment Voucher',
        'app_model':app_model,
        'beneficiary':beneficiary,
        'form':form
        
    }
    return render(request,template,context)

@permission_required('dms.custom_create_document',raise_exception = True)
@login_required(login_url='authentication:login')
def resend_code(request,item_id):
    beneficiary = PaymentVoucherBeneficiary.objects.get(id=item_id)
    code = random_with_N_digits(6)
    beneficiary.code = code
    beneficiary.save()
    item = PaymentVoucher.objects.get(id=beneficiary.pv_id)
    staff = User.objects.get(id=beneficiary.staff.id)
    IndividualResendCodeNotification(item,staff,code).start()
    messages.info(request,'Funds Release Code Resent')
    return redirect('accounting:comfirm-code',beneficiary.id) 


@permission_required('dms.custom_create_document',raise_exception = True)
@login_required(login_url='authentication:login')
def make_payment(request,item_id):
    beneficiary = PaymentVoucherBeneficiary.objects.get(id=item_id)
    pv = PaymentVoucher.objects.get(id=beneficiary.pv_id.id)
    payable = Payables.objects.get(pv_id = pv.id)
    if beneficiary.amount_received == beneficiary.amount:
        pass
    else:
        beneficiary.amount_received += beneficiary.amount
    beneficiary.status = 'Amount Paid'
    beneficiary.save()
    # if payable.amount_paid == beneficiary.amount:
    #     pass
    # else:
    payable.amount_paid +=  beneficiary.amount
    payable.save()
    if pv.document:
            dby = f" {pv.currency_id.symbol } { beneficiary.amount_received } paid to {beneficiary.staff.first_name } {beneficiary.staff.last_name } --- {beneficiary.staff.grade} by {request.user.first_name} {request.user.last_name} ---- {request.user.grade} "
            Documenttimeline.objects.get_or_create(document_id=pv.document,timeline_comment = dby ,staff= request.user)
    
    by=f"{pv.currency_id.symbol } { beneficiary.amount_received } paid to {beneficiary.staff.first_name } {beneficiary.staff.last_name } --- {beneficiary.staff.grade} by  {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
    Pvtimeline.objects.get_or_create(pv_id=pv,timeline_comment=by,staff=request.user)
    if payable.balance <= 0.00:
        pv.status = 'Paid'
        pv.save()
        payable.status = 'Amount Paid'
        payable.save()
        by=f"All Funds paid by  {request.user.first_name} {request.user.last_name} ---- {request.user.grade}"
        Pvtimeline.objects.get_or_create(pv_id=pv,timeline_comment=by,staff=request.user)

        if pv.document:
            dby = f"All Funds Paid by {request.user.first_name} {request.user.last_name} ---- {request.user.grade} "
            Documenttimeline.objects.get_or_create(document_id=pv.document,timeline_comment = dby ,staff= request.user)
#         
    staff = User.objects.get(id=beneficiary.staff.id)
    item = PaymentVoucher.objects.get(id=beneficiary.pv_id.id)
    IndividualPaymentNotification(item,staff).start()
    AccountHodNotificationThread(item).start()
    messages.info(request,'Payment Made')
    return redirect('accounting:list-pv-beneficiary',item.id) 
        
    


    # by=f"Cheque Number Updated From {item.cheque_number} To {cheque} by {request.user.first_name} {request.user.last_name} ---- {request.user.grade} "
    #                 Pvtimeline.objects.get_or_create(pv_id=item,timeline_comment=by,staff=request.user)
    #                 if item.document:
    #                     dby = f"Pv Cheque Number Updated From {item.cheque_number} To {cheque} by {request.user.first_name} {request.user.last_name} ---- {request.user.grade} and Yet To Be Recieved By Cashier"
    #                     Documenttimeline.objects.get_or_create(document_id=item.document,timeline_comment = dby ,staff= request.user)
    #                 item.cheque_number_date =check_date
    #                 item.cheque_number =cheque