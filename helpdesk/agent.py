# from msilib.schema import Error
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
import os

@login_required(login_url='authentication:login')
def load_subcategory(request):
    ipsascategory = request.GET.get('ipsascategory')
    subcategory = SubCategory.objects.filter(ipsascategory=ipsascategory).order_by('name')
    return render(request, 'authentication/district_dropdown_list.html', {'district': subcategory})

@login_required(login_url='authentication:login')
def load_user(request):
    subcostcenter = request.GET.get('subcostcenter')
    users = User.objects.filter(sub_division=subcostcenter).order_by('last_name')
    return render(request, 'authentication/user_dropdown_list.html', {'users': users})

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_agent')
def agent(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    agent_list = Agent.objects.all()
    template = 'helpdesk/agent/agent.html'
    context = {
        'agent_list': agent_list ,
        'heading': 'List of Agents',
        'pageview': 'Agents',
        'app_model':app_model
    }
    return render(request,template,context)


@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_agent')
def add_agent(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = AgentForm(request.POST,request=request)
        if form.is_valid():
            costcenter = form.cleaned_data['costcenter']
            subcostcenter = form.cleaned_data['subcostcenter']
            agent = form.cleaned_data['agent']
            team = form.cleaned_data['team']
            level = form.cleaned_data['level']
            agent = Agent.objects.get_or_create(costcenter=costcenter,subcostcenter=subcostcenter,agent=agent,team=team,level=level)
            messages.info(request,'Agent Saved')
            return redirect('helpdesk:agent-list')
    else:
        form = AgentForm(request=request)

    template = 'helpdesk/agent/create-agent.html'
    context = {
        'form':form,
        'heading': 'New Level',
        'pageview': 'List of Levels',
        'app_model':app_model
    }
    return render(request,template,context)

login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_agent')
def edit_agent(request,agent_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    agent=Agent.objects.get(id=agent_id)
    if request.method == 'POST':
        form = AgentForm(request.POST,request=request,instance=agent)
        if form.is_valid():
            form.save()
            
            messages.info(request,'Agent Updated')
            return redirect('helpdesk:agent-list')
    else:
        form = AgentForm(instance=agent,request=request)

    template = 'helpdesk/agent/create-agent.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Agents',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_agent')
def delete_agent(request,agent_id):
    agent=Agent.objects.get(id=agent_id)
    agent.delete()
    messages.error(request,'Agent Deleted')
    return redirect('helpdesk:agent-list')


@login_required(login_url='authentication:login')
def agent_upload(request):
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
                DataUploadThread(dbframe,action='agent').start()
                messages.success(request,'Agent Upload Started')
                
            else:
                messages.error(request, 'File not found.')
            return redirect('helpdesk:agent-list')

    else:
        form = UploadFileForm()

    template = 'authentication/upload.html'
    context = {
        'form': form,
    }
    return render(request, template, context)