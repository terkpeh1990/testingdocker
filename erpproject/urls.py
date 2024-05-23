"""erpproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from erpproject import views

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.DashboardView,name='dashboard'), 
    path('authentication/', include('authentication.urls', namespace='authentication')), 
    path('inventory/', include('inventory.urls', namespace='inventory')), 
    path('company/', include('company.urls', namespace='company')), 
    path('accounting/',include('accounting.urls', namespace='accounting')),
    path('dms/',include('dms.urls',namespace='dms')),
    path('supplychain/',include('supply_chain.urls',namespace='supplychain')),
    path('purchaseorder/',include('purchase_order.urls',namespace='purchaseorder')),
    path('fixedassets/',include('fixedassets.urls',namespace='fixedassets')),
    path('helpdesk/',include('helpdesk.urls',namespace='helpdesk')),
]

handler404 = 'authentication.auth.error_404_view'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

