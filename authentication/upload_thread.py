import threading
from django.http import request
from .models import *
from django.contrib import messages
from django.shortcuts import redirect,render
from django.utils.datastructures import MultiValueDictKeyError
from .models import *
from django.contrib.auth.hashers import make_password

class  GradeThread(threading.Thread):
    def __init__(self, dbframe):
        self.data = dbframe 
       
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                try:
                    tenant= Tenants.objects.get(name=i.Institutuion.title().strip())
                except Tenants.DoesNotExist:
                    tenant= Tenants.objects.create(name=i.Institutuion.title().strip())
                Grade.objects.get_or_create(name=i.Grade.title().strip(),tenant_id=tenant)
        except IOError:
            print('fail')
            pass


class  UserThread(threading.Thread):
    def __init__(self, dbframe):
        self.data = dbframe 
       
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                try:
                    tenant= Tenants.objects.get(name=i.Institutuion.title().strip())
                except Tenants.DoesNotExist:
                    tenant= Tenants.objects.create(name=i.Institutuion.title().strip())
                try:
                    devision = Devision.objects.get(name=i.Devision.title().strip(),tenant_id=tenant)
                except Devision.DoesNotExist:
                    devision = Devision.objects.create(name=i.Devision.title().strip(),tenant_id=tenant)
                try:
                    sub_devision =Sub_Devision.objects.get(name=i.SubDevision.title().strip(),devision=devision)
                except Sub_Devision.DoesNotExist:
                    sub_devision = Sub_Devision.objects.create(name=i.SubDevision.title().strip(),devision=devision)
                
                try:
                    group = Group.objects.get(name=i.Group.title().strip())
                except Group.DoesNotExist:
                    group = Group.objects.create(name=i.Group.title().strip())
                pp ='password'
                password = make_password(pp)
                try:
                    user = User.objects.get(staffid=str(i.Staffid).strip(),tenant_id=tenant)
                except User.DoesNotExist:
                    phone= "0"+str(i.Phonenumber).strip()
                    user = User.objects.create(staffid=str(i.Staffid).strip(),last_name=i.Lastname.title().strip(),first_name=i.Firstname.title().strip(),phone_number=phone,devision=devision, sub_division= sub_devision,group=group,email=i.Email.lower().strip(),password=password,is_active=True,is_new=True,tenant_id=tenant)
                user.groups.add(group)
        except IOError:
            print('fail')
            pass

