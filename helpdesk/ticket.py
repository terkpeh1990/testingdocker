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
from authentication.permission import user_belongs_to_group_with_permission
import datetime
import datetime
import pytz
from django.db.models import Sum ,Q,Count,Case, When, F,CharField,IntegerField,Value
from django.db.models.functions import Concat


@login_required(login_url='authentication:login')
def allticket(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if user_belongs_to_group_with_permission(user=request.user,app_label='helpdesk',codename='custom_helpdesk') or request.user.has_perm('helpdesk.custom_helpdesk') or request.user.has_perm('helpdesk.custom_solve_ticket') or user_belongs_to_group_with_permission(user=request.user,app_label='helpdesk',codename='custom_solve_ticket'):
        ticket_list = Ticket.objects.all().order_by('-id')
    else: 
        ticket_list = Ticket.objects.filter(ticketuser=request.user).order_by('-id')
    template = 'helpdesk/ticket/ticket.html'
    context = {
        'ticket_list': ticket_list ,
        'heading': 'List of Ticket',
        'pageview': 'Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_solve_ticket')
def ontime_ticket(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    agent = Agent.objects.get(agent = request.user)
    ticket_list = Ticket.objects.filter(completeddate__lte= F('expecteddate')).order_by('-id')
    template = 'helpdesk/ticket/ticket.html'
    context = {
        'ticket_list': ticket_list ,
        'heading': 'List of Ticket',
        'pageview': 'Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_solve_ticket')
def notontime_ticket(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    agent = Agent.objects.get(agent = request.user)
    ticket_list = Ticket.objects.filter(completeddate__gt=F('expecteddate')).order_by('-id')
    template = 'helpdesk/ticket/ticket.html'
    context = {
        'ticket_list': ticket_list ,
        'heading': 'List of Ticket',
        'pageview': 'Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_solve_ticket')
def open_ticket(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    agent = Agent.objects.get(agent = request.user)
    ticket_list = Ticket.objects.filter(completeddate__isnull=True).order_by('-id')
    template = 'helpdesk/ticket/ticket.html'
    context = {
        'ticket_list': ticket_list ,
        'heading': 'List of Ticket',
        'pageview': 'Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_solve_ticket')
def agentticket(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    agent= Agent.objects.get(agent=request.user)
    ticket_list = AgentTicket.objects.filter(agent= agent).order_by('-id')
    template = 'helpdesk/ticket/agent-tickets.html'
    context = {
        'ticket_list': ticket_list ,
        'heading': 'List of Ticket',
        'pageview': 'Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_ticket')
def add_ticket(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if request.method == 'POST':
        form = TicketForm(request.POST,request=request)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            costcenter = form.cleaned_data['costcenter']
            subcostcenter = form.cleaned_data['subcostcenter']
            if request.user.has_perm('helpdesk.custom_helpdesk') or user_belongs_to_group_with_permission(user=request.user,app_label='helpdesk',codename='custom_helpdesk'):
                ticketuser = form.cleaned_data['ticketuser']
            else:
                ticketuser = request.user
            ticket,created=Ticket.objects.get_or_create(subject=subject,description=description,costcenter=costcenter,subcostcenter=subcostcenter,ticketuser=ticketuser)
            messagebody =[
                'Dear ' +ticket.ticketuser.last_name+ ' ' + ticket.ticketuser.first_name +','+'\nYour ticket with the following details' 
                
                '\n\nTicket Number : ' + str(ticket.id),
                'Subject : ' + ticket.subject,
                '\nwill be prioritized, assigned and tracked to completion.',
                '\nYou will be informed when completed.',
                'Thank You',
            ]
            m = messagebody
            message =  "\n".join(m)
            user = ticket.ticketuser
            MessageThread(message,user).start()
            messages.info(request,'Ticket Created')
            return redirect('helpdesk:ticket-detail', ticket.id )
    else:
        form = TicketForm(request=request)

    template = 'helpdesk/ticket/create-ticket.html'
    context = {
        'form':form,
        'heading': 'New Ticket',
        'pageview': 'List of Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_ticket')
def edit_ticket(request,ticket_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    ticket=Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST,request=request,instance=ticket)
        if form.is_valid():
            ticket=form.save(commit=False)
            costcenter = form.cleaned_data['costcenter']
            subcostcenter = form.cleaned_data['subcostcenter']
            if request.user.has_perm('helpdesk.custom_helpdesk') or user_belongs_to_group_with_permission(user=request.user,app_label='helpdesk',codename='custom_helpdesk'):
                ticketuser = form.cleaned_data['ticketuser']
            else:
                
                ticketuser = request.user
            
            ticket.costcenter = costcenter
            ticket.subcostcenter = subcostcenter
            ticket.ticketuser = ticketuser
            ticket.save()
            messages.info(request,'Ticket Updated')
            return redirect('helpdesk:ticket-detail', ticket.id)
    else:
        form = TicketForm(instance=ticket,request=request)

    template = 'helpdesk/ticket/create-ticket.html'
    context = {
        'form':form,
        'heading': 'Update',
        'pageview': 'List of Tickets',
        'app_model':app_model,
       
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_ticket')
def ticketdetail(request,ticket_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    ticket=Ticket.objects.get(id=ticket_id)
    ticketassignment = AgentTicket.objects.filter(ticket=ticket.id).order_by('-id')
    comment = AgentComment.objects.filter(ticket=ticket.id).order_by('-id')
    template = 'helpdesk/ticket/ticket-detail.html'
    context = {
        'ticket':ticket,
        'ticketassignment':ticketassignment,
        'comment':comment,
        'heading': 'Detail',
        'pageview': 'List of Tickets',
        'app_model':app_model, 
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_ticket')
def agentticketdetail(request,ticket_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    agentticket= AgentTicket.objects.get(id=ticket_id)
    ticket=Ticket.objects.get(id=agentticket.ticket.id)
    ticketassignment = AgentTicket.objects.filter(ticket=ticket.id).order_by('-id')
    comment = AgentComment.objects.filter(ticket=ticket.id).order_by('-id')
    template = 'helpdesk/ticket/agent-ticket-detail.html'
    context = {
        'ticket':ticket,
        'ticketassignment':ticketassignment,
        'comment':comment,
        'heading': 'Detail',
        'pageview': 'List of Tickets',
        'app_model':app_model, 
        'agentticket':agentticket,
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_solve_ticket')
def assigned_ticket(request,ticket_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    ticket=Ticket.objects.get(id=ticket_id)
    form = AssignedTicketForm(request.POST,request=request)
    if form.is_valid():
        level = form.cleaned_data['level']
        agent = form.cleaned_data['agent']
        priority = form.cleaned_data['priority']
        assign=AgentTicket.objects.create(level=level,agent=agent,priority=priority)
        assign.assigneddate = timezone.now()
        assign.assignedtime = datetime.datetime.now().time()
        assign.ticket = ticket

        assign.status = 'Assigned'
        if assign.priority == 'High':
            assign.expected_date = assign.assigneddate + datetime.timedelta(days=1)
        elif assign.priority == 'Medium':
            assign.expected_date = assign.assigneddate + datetime.timedelta(days=2)
        else:
            assign.expected_date = assign.assigneddate + datetime.timedelta(days=3)
        assign.save()
        ticket.status = 'Assigned'
        ticket.priority=assign.priority 
        ticket.expecteddate = assign.expected_date
        ticket.assigndate = assign.assigneddate
        ticket.save()
        messagebody =[
                'Dear ' +ticket.ticketuser.last_name+ ' ' + ticket.ticketuser.first_name +','+'\nTicket with the following details' 
                
                '\n\nTicket Number : ' + str(ticket.id),
                'Subject : ' + ticket.subject,
                'Priority : '+ ticket.priority,
                '\nhas been assigned to you.',
                'Thank You',
            ]
        m = messagebody
        message =  "\n".join(m)
        user = assign.agent.agent
        MessageThread(message,user).start()
        messages.info(request,'Ticket Assigned')
        return redirect('helpdesk:ticket-detail', ticket.id)
    else:
        form = AssignedTicketForm(request=request)

    template = 'helpdesk/ticket/assign-ticket.html'
    context = {
        'form':form,
        'heading': 'Ticket',
        'pageview': 'List of Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_solve_ticket')
def excalate_ticket(request,ticket_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    ticket=Ticket.objects.get(id=ticket_id)
    form = AssignedTicketForm(request.POST,request=request)
    if form.is_valid():
        level = form.cleaned_data['level']
        agent = form.cleaned_data['agent']
        priority = form.cleaned_data['priority']
        assign,created=AgentTicket.objects.get_or_create(level=level,agent=agent,priority=priority)
        assign.assigneddate = timezone.now()
        assign.assignedtime = datetime.datetime.now().time()
        assign.ticket =ticket
        assign.status = 'Escalated'
        if assign.priority == 'High':
            assign.expected_date = assign.assigneddate + datetime.timedelta(days=1)
        elif assign.priority == 'Medium':
            assign.expected_date = assign.assigneddate + datetime.timedelta(days=2)
        else:
            assign.expected_date = assign.assigneddate + datetime.timedelta(days=3)
        assign.save()
        ticket.status = 'Escalated'
        ticket.priority=assign.priority 
        ticket.save()
        messagebody =[
                'Dear ' +ticket.ticketuser.last_name+ ' ' + ticket.ticketuser.first_name +','+'\nTicket with the following details' 
                
                '\n\nTicket Number : ' + str(ticket.id),
                'Subject : ' + ticket.subject,
                'Priority : '+ ticket.priority,
                '\nhas been escalated to you.',
                'Thank You',
            ]
        m = messagebody
        message =  "\n".join(m)
        user = assign.agent.agent
        MessageThread(message,user).start()
        messages.info(request,'Ticket Assigned')
        return redirect('helpdesk:ticket-detail', ticket.id)
    else:
        form = AssignedTicketForm(request=request)

    template = 'helpdesk/ticket/assign-ticket.html'
    context = {
        'form':form,
        'heading': 'Ticket',
        'pageview': 'List of Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_solve_ticket')
def comment_ticket(request,ticket_id):
    if request.user.is_superuser:
        app_model = Companymodule.objects.all()
    else:
        app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    agentticket= AgentTicket.objects.get(id=ticket_id)
    print(agentticket.agent)
    ticket=Ticket.objects.get(id=agentticket.ticket.id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.cleaned_data['comment']
        agent = Agent.objects.get(agent = request.user)
        coment,created=AgentComment.objects.get_or_create(ticket=ticket,comment=comment,agent=agentticket.agent)
        messages.info(request,'Comment Recorded')
        return redirect('helpdesk:agent-ticket-detail', agentticket.id)
    else:
        form = CommentForm()

    template = 'helpdesk/ticket/comment-ticket.html'
    context = {
        'form':form,
        'heading': 'Ticket',
        'pageview': 'List of Tickets',
        'app_model':app_model
    }
    return render(request,template,context)

@login_required(login_url='authentication:login')
def load_agent(request):
    level = request.GET.get('level')
    agent = Agent.objects.filter(level=level)
    return render(request, 'helpdesk/ticket/loadagent.html', {'agent': agent})

def closeticket(request,ticket_id):
    ticket= AgentTicket.objects.get(id=ticket_id)
    ticket.status = 'Closed'
    ticket.ticket.status = 'Closed'
    ticket.ticket.save()
    ticket.save()
    messagebody =[
                'Dear ' +ticket.ticket.ticketuser.last_name+ ' ' + ticket.ticket.ticketuser.first_name +','+'\nWe are pleased to inform you that your ticket with the following details' 
                
                '\n\nTicket Number : ' + str(ticket.ticket.id),
                'Subject : ' + ticket.ticket.subject,
                'Priority : '+ ticket.ticket.priority,
                '\nhas been resolved Successfully.',
                'Thank You',
            ]
    m = messagebody
    message =  "\n".join(m)
    user = ticket.ticket.ticketuser
    MessageThread(message,user).start()
    messages.info(request,'Ticket Closed')
    return redirect('helpdesk:agent-ticket-detail', ticket.id)

@login_required(login_url='authentication:login')
@permission_required('helpdesk.custom_create_ticket')
def delete_ticket(request,ticket_id):
    ticket= Ticket.objects.get(id=ticket_id)
    ticket.delete()
    messages.error(request,'Ticket Deleted')
    return redirect('helpdesk:ticket-list')
    

def ticketdashboard(request):
    app_model = Companymodule.objects.filter(tenant_id = request.user.devision.tenant_id.id)
    if user_belongs_to_group_with_permission(user=request.user,app_label='helpdesk',codename='custom_helpdesk') or request.user.has_perm('helpdesk.custom_helpdesk') or request.user.has_perm('helpdesk.custom_solve_ticket') or user_belongs_to_group_with_permission(user=request.user,app_label='helpdesk',codename='custom_solve_ticket'):
        tickets = Ticket.objects.all()
        status_based_ticket = Ticket.objects.values('status').annotate(total=Count('id'))
        cost_center_based_statistics = Ticket.objects.values('costcenter__name').annotate(total=Count('id')).order_by('total')
    else: 
        status_based_ticket = Ticket.objects.filter(ticketuser=request.user).values('status').annotate(total=Count('id'))
        tickets=Ticket.objects.filter(ticketuser=request.user).order_by('id')
        cost_center_based_statistics = Ticket.objects.filter(ticketuser=request.user).values('costcenter__name').annotate(total=Count('id')).order_by('total')
    agents_tickets = AgentTicket.objects.all()
    total_ticket = tickets.count()
    total_ticket_ontime = tickets.filter(completeddate__lte=F('expecteddate')).count()
    total_ticket_notontime = tickets.filter(completeddate__gt=F('expecteddate')).count()
    agent_based_statistics = AgentTicket.objects.values(
                                fullname=Concat('agent__agent__first_name', Value(' '), 'agent__agent__last_name', output_field=models.CharField())
                                ).annotate(
                                    total=Count('id'),
                                    assigned=Count(Case(When(status='Assigned', then=1), output_field=IntegerField())),
                                    escalated=Count(Case(When(status='Escalated', then=1), output_field=IntegerField())),
                                    closed=Count(Case(When(status='Closed', then=1), output_field=IntegerField()))
                                )
    
    if tickets:
        top_10_ticket = tickets[:10]
    else:
        top_10_ticket = tickets

    template = 'dashboard/helpdesk.html'
    context = {
        
        'heading': 'Dashboard',
        'pageview': 'Dashboard',
        'app_model':app_model,
        'status_based_ticket':status_based_ticket,
        'total_ticket':total_ticket,
        'total_ticket_ontime':total_ticket_ontime,
        'total_ticket_notontime':total_ticket_notontime,
        'agent_based_statistics': agent_based_statistics,
        'cost_center_based_statistics':cost_center_based_statistics,
        'top_10_ticket':top_10_ticket
        

    }
    return render(request,template,context)
    
