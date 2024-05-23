
from django.http import request
from django.shortcuts import redirect, render
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from appsystem.models import *


# utillity

@login_required(login_url='authentication:login')
def DashboardView(request):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
        
    template = 'dashboard/index.html'
    context = {
        # 'app_model ': app_model ,
        'heading': 'Dashboard',
        'pageview': 'Dashboards',
        'app_model':app_model
    }
    return render(request,template,context)