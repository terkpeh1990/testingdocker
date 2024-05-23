from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from appsystem.models import *
from authentication.forms import *

@login_required(login_url='authentication:login')
@permission_required('supply_chain.custom_view_budget',raise_exception = True)
def annualbudget(request):
    
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    budget_list = Annual_Budget.objects.all()
    template = 'supplychain/budget/budget.html'
    context = {
        'budget_list': budget_list,
        'heading': 'List of Annual Budgets',
        'pageview': 'Annual Budgets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('supply_chain.custom_create_budget',raise_exception = True)
def add_annualbudget(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    budget_list = Annual_Budget.objects.all().order_by('id')
    print(len(budget_list))
    if request.method == 'POST':       
        form = BudgetForm(request.POST)
        if form.is_valid():    
            if budget_list and len(budget_list) > 0:
                last_record = budget_list.latest('id')
                last_record.status = 'In Active'
                last_record.save()
            start=form.cleaned_data['start']
            budget=form.save(commit=False)
            budget.period = start.year
            budget.status= 'Active'
            budget.save()
            
            messages.info(request,'Annual Budget Created')
            return redirect('supplychain:annualbudget-list')
    else:
        form =  BudgetForm()

    template = 'supplychain/budget/create-budget.html'
    context = {
        'form':form,
        'heading': 'New',
        'pageview': 'List of Annual Budget',
        'app_model':app_model
    }
    return render(request,template,context)



@login_required(login_url='authentication:login')
@permission_required('supply_chain.custom_create_budget',raise_exception = True)
def edit_annualbudget(request,budget_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    budget =  Annual_Budget.objects.get(id=budget_id)
    if request.method == 'POST':
        
        form = BudgetForm(request.POST,instance=budget)
        if form.is_valid():
            start=form.cleaned_data['start']
            updatedbudget=form.save(commit=False)
            updatedbudget.period = start.year
            updatedbudget.save()
            messages.info(request,'Annual Budget Updated')
            return redirect('supplychain:annualbudget-list')
    else:
        form =  BudgetForm(instance=budget)

    template = 'supplychain/budget/create-budget.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Annual Budget',
        'app_model':app_model
    }
    return render(request,template,context)