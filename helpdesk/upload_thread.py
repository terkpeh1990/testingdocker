import threading
from django.http import request
from .models import *
from django.contrib import messages
from django.shortcuts import redirect,render
from django.utils.datastructures import MultiValueDictKeyError
from authentication.models import User
from company.models import Tenants
from erpproject.settings import  endPoint,key,Sender_Id, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import requests
from decimal import Decimal
from django.core.mail import send_mail, EmailMessage

 
class  DataUploadThread(threading.Thread):
    def __init__(self, dbframe,action):
        self.data = dbframe 
        self.action = action
       
        threading.Thread.__init__(self)

    def team(self,team):
       team,created = Teams.objects.get_or_create(name=team)
       return team

    def level(self,level):
        level,created = Level.objects.get_or_create(name=level)
        return level
    
    def getuseragent(self,staffid):
        user = User.objects.get(staffid=staffid)
        return user
    
    def agent(self,getteam,getlevel,getuser):
        agent,created = Agent.objects.get_or_create(agent=getuser,team=getteam,level=getlevel)
        agent.costcenter = agent.agent.devision
        agent.subcostcenter = agent.agent.sub_division
        agent.save()
        return agent

    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                if self.action == 'team':
                    team = i.Team.title().strip()
                    self.team(team)
                elif self.action == 'level':
                    name = i.Level.title().strip()
                    self.level(name)
                elif self.action == 'agent':
                    level = i.Level.title().strip()
                    getlevel=self.level(level)

                    team = i.Team.title().strip()
                    getteam=self.team(team)

                    staffid = i.Staffid
                    getuser = self.getuseragent(staffid)
                    agent = self.agent(getteam,getlevel,getuser)
                else:
                    pass
        except IOError:
            print('fail')
            pass


class  MessageThread(threading.Thread):
    def __init__(self,message,user):
        self.message =message
        self.user =user
        
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        phone ='233'+self.user.phone_number
        email = self.user.email
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+self.message)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        try:
            subject = "Ticket Generation"
            message = self.message
            sender = EMAIL_HOST_USER
            to = [email]
            send_mail(subject, message, sender, to, fail_silently=False)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
        
       
