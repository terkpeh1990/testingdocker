from django.db import models
from company.models import *
from authentication.models import User
import datetime
from django.utils import timezone

# Create your models here.
class Teams(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        
        db_table = 'Teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        permissions = [
            ("custom_create_team", "Can Create Helpdesk Team"),
        ]

        
    def __str__(self):
        return f"{self.name}"

class Level(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        
        db_table = 'Levels'
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'
        

        
    def __str__(self):
        return f"{self.name}"

class Agent(models.Model):
    costcenter = models.ForeignKey('company.Devision', related_name='agentcostcenter', on_delete=models.CASCADE,null=True)
    subcostcenter = models.name = models.ForeignKey('company.Sub_Devision', related_name='agentsubcostcenter', on_delete=models.CASCADE,null=True)
    agent = models.ForeignKey(User,related_name='agent', on_delete=models.CASCADE)
    team = models.ForeignKey(Teams,related_name='agentteam', on_delete=models.CASCADE)
    level = models.ForeignKey(Level,related_name='agentlevel', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.agent.first_name } { self.agent.last_name}"
        

    class Meta:
        db_table = 'Agent'
        managed = True
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'
        permissions = [
            ("custom_create_agent", "Can Create Helpdesk Agent"),
        ]

class Ticket(models.Model):
    status = (
            ('Pending', 'Pending'),
            ('Assigned', 'Assigned'),
            ('Resolved', 'Resolved'),
            ('Escalated', 'Escalated'),
            ('Closed', 'Closed'),
        )
    
    priority = (
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
        )

    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    costcenter = models.ForeignKey('company.Devision', related_name='ticketcostcenter', on_delete=models.CASCADE,null=True)
    subcostcenter = models.ForeignKey('company.Sub_Devision', related_name='ticketsubcostcenter', on_delete=models.CASCADE,null=True)
    ticketuser = models.ForeignKey('authentication.User', related_name='ticketuser', on_delete=models.CASCADE,null=True)
    ticket_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50,choices=status,default='Pending',null=True)
    priority =  models.CharField(max_length=50,choices=priority,default='Low',null=True)
    assigndate = models.DateTimeField(null=True, blank=True)
    completeddate = models.DateTimeField(null=True, blank=True)
    expecteddate = models.DateTimeField(null=True, blank=True)
    completed_days = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if not self.id:
            self.ticket_date = timezone.now()

        super(Ticket, self).save(*args, **kwargs)  

    class Meta:
        db_table = 'Tickets'
        managed = True
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        permissions = [
            ("custom_create_ticket", "Can Create Ticket"),
            ("custom_solve_ticket", "Can solve ticket"),
            ("custom_helpdesk", "Can Be Helpdesk"),
        ]

class AgentTicket(models.Model):
    status = (
            ('Assigned', 'Assigned'),
            ('Resolved', 'Resolved'),
            ('Escalated', 'Escalated'),
            ('Closed', 'Closed'),
        )
    
    priority = (
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
        )
    ticket = models.ForeignKey('Ticket', related_name='agentticket', on_delete=models.CASCADE,null=True)
    agent = models.ForeignKey('Agent', related_name='helpdeskagent', on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=50,choices=status,null=True)
    priority =  models.CharField(max_length=50,choices=priority,default='Low',null=True)
    level = models.ForeignKey('Level', related_name='assignlevel', on_delete=models.CASCADE,null=True)
    assigneddate = models.DateTimeField(null=True, blank=True)
    completeddate = models.DateTimeField(null=True, blank=True)
    assignedtime = models.TimeField(null=True, blank=True)
    completedtime = models.TimeField(null=True, blank=True)
    timetaken = models.DateField(null=True, blank=True)
    expected_date = models.DateTimeField(null=True, blank=True)
    completed_days = models.DurationField(null=True, blank=True)
    elapsed_time = models.DurationField(null=True, blank=True)
    expected_days = models.DurationField(null=True, blank=True)
    use_date = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        
        if self.status == 'Closed':
            self.completeddate = timezone.now()
            self.ticket.completeddate=timezone.now()
            if self.completeddate and self.assigneddate:
                delta2 =self.completeddate - self.assigneddate
                delta1 = self.ticket.completeddate - self.ticket.ticket_date
                self.completed_days = delta2-datetime.timedelta(microseconds=delta2.microseconds)
                self.ticket.completed_days = delta1-datetime.timedelta(microseconds=delta1.microseconds)
            self.ticket.save()

        super(AgentTicket, self).save(*args, **kwargs)  
    

   

    def __str__(self):
        return self.ticket.subject

    class Meta:
        db_table = 'AgentTicket'
        managed = True
        verbose_name = 'AgentTicket'
        verbose_name_plural = 'AgentTickets'

class AgentComment(models.Model):
    ticket = models.ForeignKey('Ticket', related_name='agentcomment', on_delete=models.CASCADE,null=True)
    agent = models.ForeignKey('Agent', related_name='solution', on_delete=models.CASCADE,null=True)
    comment = models.CharField(max_length=1200)
    commentdate = models.DateField(null=True, blank=True)
    commenttime = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.commentdate = datetime.datetime.now()
        self.commenttime = datetime.datetime.now().time()
        super(AgentComment, self).save(*args, **kwargs)  
   
    def __str__(self):
        return self.comment

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'AgentComment'
        verbose_name_plural = 'AgentComments'


# class Technicias(models.Model):
#     technician = models.ForeignKey(User, on_delete=models.CASCADE)
#     team = models.ForeignKey(Teams, on_delete=models.CASCADE)
#     tenant_id = models.ForeignKey(
#         Tenants, blank=True, null=True, related_name = 'technicains',on_delete=models.CASCADE)
   
#     class Meta:
        
#         db_table = 'Technicians'
#         verbose_name = 'Technician'
#         verbose_name_plural = 'Technicians'

#     def __str__(self):
#         return f"{self.technician.first_name } { self.technician.last_name} ---- {self.tenant_id}"

# class Tickets(models.Model):
#     ess = (
#         ('Escalate', 'Escalate'),
#     )
#     id = models.CharField(max_length=200, primary_key=True)
#     name = models.ForeignKey(
#         Profile, null=True, blank=True, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=200)
#     description = models.CharField(max_length=200)
#     region = models.ForeignKey(
#         Region, blank=True, null=True, on_delete=models.CASCADE)
#     district = models.ForeignKey(
#         District, blank=True, null=True, on_delete=models.CASCADE)
#     category = models.ForeignKey(
#         Category, null=True, blank=True, on_delete=models.CASCADE)
#     ticket_category = models.ForeignKey(
#         Ticket_category, null=True, blank=True, on_delete=models.CASCADE)
#     status = models.ForeignKey(
#         Status, null=True, blank=True, on_delete=models.CASCADE)
#     astatus = models.ForeignKey(
#         agent_Status, null=True, blank=True, on_delete=models.CASCADE)
#     prority = models.ForeignKey(
#         Prority, null=True, blank=True, on_delete=models.CASCADE)
#     agent = models.ForeignKey(Technician, null=True,
#                               blank=True, on_delete=models.CASCADE)
#     agent_team = models.ForeignKey(
#         Team, null=True, blank=True, on_delete=models.CASCADE)
#     ticket_date = models.DateField()
#     ticket_time = models.TimeField()
#     use_date = models.DateTimeField()
#     expected_date = models.DateField(null=True, blank=True)
#     expected_days = models.DurationField(null=True, blank=True)
#     escalated = models.CharField(max_length=60, choices=ess)
#     remarks = models.CharField(max_length=200, null=True, blank=True)
#     close_date = models.DateField(null=True, blank=True)
#     completed_days = models.DurationField(null=True, blank=True)
#     elapsed_time = models.DurationField(null=True, blank=True)
#     history = HistoricalRecords()

