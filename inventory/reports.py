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
from company.models import *
import datetime
from django.db.models import Sum ,Q,Count,F
from datetime import date, timedelta
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
from erpproject.settings import  endPoint,key,Sender_Id


@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_report',raise_exception = True)
def reportrequisition(request):
    if request.user.is_superuser:
        requisition_list = Requisition.objects.all()
        app_model = Companymodule.objects.all()
    else:
        if request.user.has_perm('inventory.custom_approve_requisition'):
            requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id,staff__sub_division = request.user.sub_division)
        elif request.user.has_perm('inventory.custom_approve_capital_requisition') or request.user.has_perm('inventory.custom_approve_consumable_requisition') or request.user.has_perm('inventory.custom_issue_requisition'):
            requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id)
        else:
            requisition_list = Requisition.objects.filter(tenant_id=request.user.devision.tenant_id.id,staff = request.user)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    
    myFilter = RequisitionFilter(request.GET, queryset=requisition_list)
    requisition_list = myFilter.qs

    template = 'inventory/reports/requisition-list.html'
    context = {
        'requisition_list': requisition_list,
        'heading': 'List of Requisition',
        'pageview': 'Requisition',
        'app_model':app_model,
        'myFilter':myFilter
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_report',raise_exception = True)
def regionrequisition(request):
    if request.user.is_superuser:
        devision = Devision.objects.all()
        requisition = devision.values('name').annotate(total=Count('reqdevisions__id')
        ).values('name','total').exclude(total__lte = 0).order_by('-total')
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        devision = Devision.objects.filter(tenant_id=request.user.devision.tenant_id.id)
        requisition = devision.values('name').annotate(total=Count('reqdevisions__id')
        ).values('name','total').exclude(total__lte = 0).order_by('-total')
   
    
    template = 'inventory/reports/requisition-statistics.html'
    context = {
        'requisition': requisition,
        'heading': 'List of Devisional Requisition',
        'pageview': 'Reports',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_report',raise_exception = True)
def districtrequisition(request):
    if request.user.is_superuser:
        sub_devision = Sub_Devision.objects.all()
        requisition = sub_devision.values('name').annotate(total=Count('reqsub_districts__id'),
        ).values('name','total').exclude(total__lte=0).order_by('-total')
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        sub_devision = Sub_Devision.objects.filter(tenant_id=request.user.devision.tenant_id.id)
        requisition = sub_devision.values('name').annotate(total=Count('reqsub_districts__id'),
        ).values('name','total').exclude(total__lte=0).order_by('-total')
    
    template = 'inventory/reports/requisition-statistics.html'
    context = {
        'requisition': requisition,
        'heading': 'List of Sub Devisional Requisition',
        'pageview': 'Reports',
        'app_model':app_model,
    
    }
    return render(request,template,context)

# @login_required(login_url='authentication:login')
# @permission_required('inventory.custom_delete_product')
def return_assets(request,assets_id):
    assets = Assets.objects.get(id=assets_id)
    assets.status = False
    assets.save()
    messages.success(request,'Assets Now Avialable')
    return redirect('inventory:assigned-assets')


@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_report',raise_exception = True)
def low_stock_alert(request):
    if request.user.is_superuser:
        low_stock=Inventory.objects.filter(avialable_quantity__lte = F('product_id__restock_level'))
        app_model = Companymodule.objects.all()
    else:
        low_stock=Inventory.objects.filter(tenant_id=request.user.devision.tenant_id,avialable_quantity__lte = F('product_id__restock_level'))
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    template = 'inventory/reports/inventory.html'
    context = {
        'low_stock': low_stock,
        'heading': 'Low Stock',
        'pageview': 'Report',
        'app_model':app_model,
    
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_report',raise_exception = True)
def expire_products(request):
    today = date.today()
    three_months_from_today = today + timedelta(days=3*30)
    if request.user.is_superuser:
        expiring_batch = Inventory_Details.objects.filter(inventory_id__tenant_id=request.user.devision.tenant_id.id,avialable_quantity__gt=0,expiring_date__lte=three_months_from_today)
        app_model = Companymodule.objects.all()
    else:
        expiring_batch= Inventory_Details.objects.filter(inventory_id__tenant_id=request.user.devision.tenant_id.id,avialable_quantity__gt=0,expiring_date__lte=three_months_from_today)
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    template = 'inventory/reports/expired.html'
    context = {
        'expiring_batch': expiring_batch,
        'heading': 'Products Already Expired or Expiring In 3 Months',
        'pageview': 'Report',
        'app_model':app_model,
    
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('authentication.custom_view_report',raise_exception = True)
def assigned_assets(request):
    if request.user.is_superuser:
        assets_list = Assigned_Assets.objects.filter(assets_id__status=True)
        app_model = Companymodule.objects.all()
    else:
        
        assets_list = FixedAsset.objects.filter(status='Assigned')
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)

    template = 'inventory/reports/assigned-assets.html'
    context = {
       
        'heading': 'List of Assigned Assets',
        'pageview': 'Report',
        'app_model':app_model,
        'assets_list':assets_list
    
    }
    return render(request,template,context)


def get_requisitions_for_product(product_id):
    requisitions = Requisition_Details.objects.filter(product_id=product_id).values('requisition_id__requisition_date', 'quantity')
    return pd.DataFrame(list(requisitions))


def forecast_out_of_stock(product_id):
    df = get_requisitions_for_product(product_id)

    # Rename the columns to fit Prophet's requirements
    df = df.rename(columns={'requisition_id__requisition_date': 'ds', 'quantity': 'y'})

    # Initialize and fit the Prophet model
    model = Prophet(daily_seasonality=False)
    model.fit(df)

    # Create future dates for prediction
    future_dates = model.make_future_dataframe(periods=365)  # Forecast for the next 365 days

    # Perform the forecast
    forecast = model.predict(future_dates)

    return forecast

def create_forecast_plot(product_id):
    forecast = forecast_out_of_stock(product_id)

    fig = go.Figure()

    # Historical data
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Historical Data'))

    # Forecasted data
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecasted Data'))

    fig.update_layout(title='Product Out of Stock Forecast',
                      xaxis_title='Date',
                      yaxis_title='Requisition Quantity')

    return fig


def forecast_view(request, product_id):
    product = Products.objects.get(pk=product_id)
    forecast_plot = create_forecast_plot(product_id)

    return render(request, 'inventory/reports/product-forcast.html', {
        'product': product,
        'forecast_plot': forecast_plot.to_html(),
    })



def check_product_stock():
    companys = Tenants.objects.all()
    url = endPoint + '&api_key=' + key
     
    for i in companys:
        products = Inventory.objects.filter(tenant_id=i.id,avialable_quantity__lte = F('product_id__restock_level'))
        item =[]
        for product in products:
            print(product.product_id.name)
            item.append(product.product_id)
        print(item)
        user = User.objects.filter(tenant_id=i.id)
        for u in user:
            if u.has_perm('authentication.custom_view_report'):
                body = [
                    
                    'Dear' + ' '+u.first_name + ' '+ u.last_name + ', ' +'the following product are running low on stock'
                    
                    '\n\nLow on Stock Summery :\n------------------------',
                    '\n'.join(item),
                    '\nThank you for using Smart ERP',
                    ]
                m = body
                message =  "\n".join(m)
                print(message)
                phone='233'+u.phone_number
                senders = Sender_Id
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+message)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
