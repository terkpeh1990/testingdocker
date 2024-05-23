from django.http import request
from django.shortcuts import redirect, render
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from appsystem.models import *
from .models import *
from authentication.models import User
from django.db.models import Sum ,Q,Count,F
from datetime import date, timedelta
from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractYear

# utillity


@login_required(login_url='authentication:login')
def InventoryDashboardView(request):
    today = date.today()
    three_months_from_today = today + timedelta(days=3*30)
    current_date = timezone.now().date()
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
        requisition_list = Requisition.objects.all()
        product_list = Inventory.objects.all()
        low_stock = Inventory.objects.filter(avialable_quantity__lte = F('product_id__restock_level'))
        user_list = User.objects.all()
        expiried_batch = Inventory_Details.objects.filter(avialable_quantity__gt=0,expiring_date=current_date)
        expiring_batch = Inventory_Details.objects.filter(avialable_quantity__gt=0,expiring_date__lte=three_months_from_today)
        supplier_list =Supplier.objects.all().order_by('-id')[:5]
        comsumable_expiring =expiring_batch.filter(inventory_id__product_id__type_of_product = "Consumables")
        user_lists = User.objects.all().order_by('-id')[:5]
        current_users = user_lists
       

    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        if request.user.has_perm('inventory.custom_approve_requisition'):
            requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id) 
            
            product_list = 0
            low_stock = 0
            user_list= 0
            expiring_batch=0
            expiried_batch=0
            supplier = 0
           
        elif request.user.has_perm('inventory.custom_approve_capital_requisition') or request.user.has_perm('inventory.custom_approve_consumable_requisition') or request.user.has_perm('inventory.custom_issue_requisition') or request.user.has_perm('inventory.custom_create_user'):
            requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id)
            product_list = Inventory.objects.filter(tenant_id=request.user.devision.tenant_id.id)
            low_stock=Inventory.objects.filter(tenant_id=request.user.devision.tenant_id.id,avialable_quantity__lte = F('product_id__restock_level'))
            user_list = User.objects.filter(tenant_id=request.user.devision.tenant_id.id)
            user_lists = User.objects.filter(tenant_id=request.user.devision.tenant_id.id).order_by('-id')[:5]
            current_users = user_lists
            expiring_batch= Inventory_Details.objects.filter(inventory_id__tenant_id=request.user.devision.tenant_id.id,avialable_quantity__gt=0,expiring_date__lte=three_months_from_today)
            # expiried_batch = Inventory_Details.objects.filter(inventory_id__tenant_id=request.user.devision.tenant_id.id,avialable_quantity__gt=0,expiring_date=current_date)
            supplier_list =Supplier.objects.filter(tenant_id=request.user.devision.tenant_id.id).order_by('-id')[:5]
            
            
        else:
            requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id,staff = request.user)
            app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
            product_list = 0
            low_stock = 0
            user_list= 0
            expiring_batch = 0
            expiried_batch = 0
            supplier = 0
    total_requisition = requisition_list.count()
    total_consumable = requisition_list.filter(classification="Consumables").count()
    total_capital = requisition_list.filter(classification="Capital").count()
    current_req = requisition_list.order_by('-id')[:10]
    # capital_by_month = requisition_list.filter(classification="Capital").annotate(month=ExtractMonth('requisition_date')).values( 'month').annotate(total_requisition=Count('id'))
    
    if product_list == 0 or low_stock == 0 :
        total_products = 0
        total_consumable_products = 0
        total_capital_products = 0
        low_stock_count=0
        user_count=0
        current_users = 0
        comsumable_expire=0
        consumable_expired =0
        supplier = 0,
        product_list =0
        product_lists =0
        active_users =0
        inactive_users =0
        comsumable_expiring = 0
        consumable_expired =0
        supplier_list=0
        expiring_batchs=0
  

    else:
        total_products = product_list.count()
        total_consumable_products = product_list.filter(product_id__type_of_product = "Consumables").count()
        total_capital_products = product_list.filter(product_id__type_of_product = "Capital").count()
        low_stock_count = low_stock.count()
        user_count = user_list.count()
        active_users = user_list.filter(is_active=True).count()
        inactive_users = user_list.filter(is_active=False).count()
        comsumable_expiring =expiring_batch.filter(inventory_id__product_id__type_of_product = "Consumables")
        # consumable_expired = expiried_batch.filter(inventory_id__product_id__type_of_product = "Consumables")
        supplier_list = supplier_list
        product_lists = product_list.filter(avialable_quantity__gt=0).order_by('-id')[:5]
        # capital_expire =expiring_batch.filter(inventory_id__product_id__type_of_product = "")

        
    requisition_status = requisition_list.values('status').annotate(total=Count('id'),
    ).values('status','total').order_by('total')
    
        
    template = 'dashboard/inventory.html'
    context = {
        'app_model ': app_model ,
        'heading': 'Dashboard',
        'pageview': 'Dashboard',
        'app_model':app_model,
        'total_requisition':total_requisition,
        'total_consumable':total_consumable,
        'total_capital':total_capital,
        'requisition_status':requisition_status,

        'total_products':total_products,
        'total_capital_products':total_capital_products,
        'total_consumable_products':total_consumable_products,
        'product_list':product_list,

        'low_stock':low_stock,
        'low_stock_count':low_stock_count,

        'user_list':user_list,
        'active_users': active_users,
        'inactive_users':inactive_users,
        'current_users':current_users,

        'expiring_batch':expiring_batch,
        'comsumable_expire':comsumable_expiring,
        # 'comsumable_expired':consumable_expired,

        'supplier_list':supplier_list,
        'product_lists':product_lists,
        'current_req':current_req 
        

    }
    return render(request,template,context)