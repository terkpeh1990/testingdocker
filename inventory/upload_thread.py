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
from fixedassets.models import *
from django.core.mail import send_mail, EmailMessage
from authentication.permission import *


class  CategoryThread(threading.Thread):
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
                Categorys.objects.get_or_create(name=i.Category.title().strip(),tenant_id=tenant)
        except IOError:
            print('fail')
            pass

class  BrandThread(threading.Thread):
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
                Brands.objects.get_or_create(name=i.Brand.title().strip(),tenant_id=tenant)
        except IOError:
            print('fail')
            pass

class  MeasureThread(threading.Thread):
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
                Unit_of_Measurement.objects.get_or_create(name=i.Unit.title().strip(),tenant_id=tenant)
        except IOError:
            print('fail')
            pass


class  ProductThread(threading.Thread):
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
                    category = Categorys.objects.get(name=i.Category.title().strip(),tenant_id =tenant)
                except Categorys.DoesNotExist:
                    category = Categorys.objects.create(name=i.Category.title().strip(),tenant_id =tenant)
                try:
                    unit = Unit_of_Measurement.objects.get(name=i.Unit.title().strip(),tenant_id =tenant)
                except Unit_of_Measurement.DoesNotExist:
                    unit = Unit_of_Measurement.objects.create(name=i.Unit.title().strip(),tenant_id =tenant)
                try:
                    product = Products.objects.get(name=i.Product.title().strip(),tenant_id =tenant)
                except Products.DoesNotExist:
                    product = Products.objects.create(category_id=category,name=i.Product.title().strip(),restock_level = i.ReorderLevel,unit_of_measurement=unit,type_of_product=i.Type.title().strip(),tenant_id=tenant)
                try:
                    inventory = Inventory.objects.get(product_id=product.id)
                    inventory.avialable_quantity += i.Quantity.strip()
                except Inventory.DoesNotExist:
                    inventory = Inventory.objects.create(product_id=product,avialable_quantity = i.Quantity,tenant_id = tenant)
                inventory_detail = Inventory_Details.objects.get_or_create(inventory_id = inventory,quantity_intake=i.Quantity,expiring_date=i.ExpiringDate)
        except IOError:
            print('fail')
            pass


class  SupplierThread(threading.Thread):
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
                Supplier.objects.get_or_create(name=i.Supplier.title().strip(),address=i.Address.title().strip(),city=i.City.title().strip(),country=i.Country.title().strip(),tenant_id=tenant)
        except IOError:
            print('fail')
            pass


class  PendingThread(threading.Thread):
    def __init__(self,requisition):
        self.requisition = requisition
        self.hod = User.objects.filter(sub_division=self.requisition.staff.sub_division)
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id

        usermessage =  'Dear ' + self.requisition.staff.last_name +' ' +self.requisition.staff.first_name  +','+'\nYour requisition with batch number' + ' '+ str(self.requisition.id) + ' '+ 'has been sent for approval. You will be notified when it is ready.'
        phone = '233'+self.requisition.staff.phone_number
        # hphone = '233'+self.hod_profile.telephone

        try:
            
            subject = "Requisition"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.requisition.staff.email]
            send_mail(subject, message, sender, to, fail_silently=False)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
        


        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        for i in self.hod:
            
            if i.has_perm('inventory.custom_approve_requisition') or user_belongs_to_group_with_permission(user=i,app_label='inventory',codename='custom_approve_requisition'):
                message = 'Dear ' + i.first_name + ' '+ i.last_name +',' + '\nRequisition with batch number' + ' '+ str(self.requisition.id) + ' '+ 'has been brougth to you attention for approval.'
                try:
                    response = requests.get(url+'&to='+i.phone_number+'&from='+senders+'&sms='+message)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Requisition"
                    message2 = message
                    sender = EMAIL_HOST_USER
                    to2 = [i.email]
                    send_mail(subject, message2, sender, to2, fail_silently=False) 
                    print('mail two success') 
                except Exception as e:
                    print(e)
                    pass


class  AwaitingThread(threading.Thread):
    def __init__(self,requisition):
        self.requisition = requisition
        self.hod = User.objects.filter(tenant_id=self.requisition.staff.tenant_id)
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id

        usermessage =  'Dear ' + self.requisition.staff.last_name +' ' +self.requisition.staff.first_name  +','+'\nYour requisition with batch number' + ' '+ str(self.requisition.id) + ' '+ 'has been sent been sent to Administration for approval. You will be notified when it is ready.'
        phone = '233'+self.requisition.staff.phone_number
        # hphone = '233'+self.hod_profile.telephone

        try:
            
            subject = "Requisition"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.requisition.staff.email]
            send_mail(subject, message, sender, to, fail_silently=False)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
        


        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        for i in self.hod:
           
            if self.requisition.classification == "Consumables":
                if user_belongs_to_group_with_permission(user=i,app_label='inventory',codename='custom_approve_consumable_requisition') or i.has_perm('inventory.custom_approve_consumable_requisition'):
                    message = 'Dear ' + i.first_name + ' '+ i.last_name +',' + '\nRequisition with batch number' + ' '+ str(self.requisition.id) + ' '+ 'has been brougth to you attention for approval.'
                    try:
                        response = requests.get(url+'&to='+i.phone_number+'&from='+senders+'&sms='+message)
                        print(response.json())
                    except IOError as e:
                        print(e)
                        pass
                    
                    try:
                        subject = "Requisition"
                        message2 = message
                        sender = EMAIL_HOST_USER
                        to2 = [i.email]
                        send_mail(subject, message2, sender, to2, fail_silently=False) 
                        print('mail two success') 
                    except Exception as e:
                        print(e)
                        pass
            elif self.requisition.classification == "Capital":
                if user_belongs_to_group_with_permission(user=i,app_label='inventory',codename='custom_approve_capital_requisition') or i.has_perm('inventory.custom_approve_capital_requisition'):
                    message = 'Dear ' + i.first_name + ' '+ i.last_name +',' + '\nRequisition with batch number' + ' '+ str(self.requisition.id) + ' '+ 'has been brougth to you attention for approval.'
                    try:
                        response = requests.get(url+'&to='+i.phone_number+'&from='+senders+'&sms='+message)
                        print(response.json())
                    except IOError as e:
                        print(e)
                        pass
                    try:
                        subject = "Requisition"
                        message2 = message
                        sender = EMAIL_HOST_USER
                        to2 = [i.email]
                        send_mail(subject, message2, sender, to2, fail_silently=False) 
                        print('mail two success') 
                    except Exception as e:
                        print(e)
                        pass
            else:
                pass


class  ApprovedThread(threading.Thread):
    def __init__(self,requisition):
        self.requisition = requisition
        self.hod = User.objects.filter(tenant_id=self.requisition.staff.tenant_id)
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id

        usermessage =  'Dear ' + self.requisition.staff.last_name +' ' +self.requisition.staff.first_name  +','+'\nYour requisition with batch number' + ' '+ str(self.requisition.id) + ' '+ 'has been approved. Please pass by the stores unit at the Head office to pickup your item(s). You will be required to provide the unique batch number before pickup'
        phone = '233'+self.requisition.staff.phone_number
        # hphone = '233'+self.hod_profile.telephone

        try:
            
            subject = "Requisition"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.requisition.staff.email]
            send_mail(subject, message, sender, to, fail_silently=False)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
        


        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        for i in self.hod:
            if user_belongs_to_group_with_permission(user=i,app_label='inventory',codename='custom_issue_requisition') or i.has_perm('inventory.custom_issue_requisition'):
                message = 'Dear ' + i.first_name + ' '+ i.last_name +',' + '\nRequisition with batch number' + ' '+ str(self.requisition.id) + ' '+ 'has been brougth to you attention for issuing.'
                try:
                    response = requests.get(url+'&to='+i.phone_number+'&from='+senders+'&sms='+message)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                try:
                    subject = "Requisition"
                    message2 = message
                    sender = EMAIL_HOST_USER
                    to2 = [i.email]
                    send_mail(subject, message2, sender, to2, fail_silently=False) 
                    print('mail two success') 
                except Exception as e:
                    print(e)
                    pass


class  StoresThread(threading.Thread):
    def __init__(self,requisition):
        self.requisition = requisition
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id

        usermessage =  'Dear ' + self.requisition.staff.last_name +' ' +self.requisition.staff.first_name  +','+'\nYour requisition with batch number' + ' '+ str(self.requisition.id) + ' '+ 'has been issued succesfully'
        phone = '233'+self.requisition.staff.phone_number
        # hphone = '233'+self.hod_profile.telephone

        # try:
            
        #     subject = "Requisition"
        #     message = usermessage
        #     sender = EMAIL_HOST_USER
        #     to = [self.requisition.staff.email]
        #     send_mail(subject, message, sender, to, fail_silently=False)
        #     print('mail one success')
        # except Exception as e:
        #     print(e)
        #     pass
        # try:
        #     subject = "Requisition"
        #     message2 = hodmessage
        #     sender = EMAIL_HOST_USER
        #     to2 = [self.hod_profile.email]
        #     send_mail(subject, message2, sender, to2, fail_silently=False) 
        #     print('mail two success') 
        # except Exception as e:
        #     print(e)
        #     pass


class  CertificationInventoryUpdateThread(threading.Thread):
    def __init__(self, job,detail,user):
        self.job = job
        self.detail = detail
        self.user = user
        threading.Thread.__init__(self)
    
    def createland(self, land):
        asset,created = FixedAsset.objects.get_or_create(classification=land.job_id.classification,description=land.description,
                        accountingrecognition=land.accountingrecognition,amotization=land.amotization,usage=land.usage,ipsascategory=land.ipsascategory,subcategory=land.subcategory,size=land.size,ghanapostgpsaddress=land.ghanapostgpsaddress,titled=land.titled,methodofacquisition=land.methodofacquisition,currentstatus='Not in Use',investmentproperty=land.investmentproperty,
                        fundsource=land.fundsource,value=land.value,usefullife=land.usefullife,product=land.product,status = 'Avialable',comments=land.comments)
        return created
    def createbuilding(self,building):
        asset,created = FixedAsset.objects.get_or_create(classification=building.job_id.classification,description=building.description,accountingrecognition=building.accountingrecognition,depreciation=building.depreciation,ipsascategory=building.ipsascategory,subcategory=building.subcategory,
                        quantity=building.quantity,ghanapostgpsaddress=building.ghanapostgpsaddress,dateplacedinservice=building.dateplacedinservice,methodofacquisition=building.methodofacquisition,currentstatus='Not in Use',conditions=building.conditions,investmentproperty=building.investmentproperty,
                        fundsource=building.fundsource,value=building.value,usefullife=building.usefullife,product=building.product,status = 'Avialable',comments=building.comments)
        return created

    def createtransport(self,transport):
        asset,created = FixedAsset.objects.get_or_create(classification=transport.job_id.classification,description=transport.description,registrationnumber=transport.registrationnumber,accountingrecognition=transport.accountingrecognition,depreciation=transport.depreciation,
                        ipsascategory=transport.ipsascategory,subcategory=transport.subcategory,quantity=transport.quantity,dateplacedinservice=transport.dateplacedinservice,colour=transport.colour,chassisno=transport.chassisno,engineserialno=transport.engineserialno,manufacturer=transport.manufacturer,model=transport.model,modelyear=transport.modelyear,methodofacquisition=transport.methodofacquisition,currentstatus='Not in Use',
                        conditions=transport.conditions,investmentproperty=transport.investmentproperty,fundsource=transport.fundsource,value=transport.value,usefullife=transport.usefullife,product=transport.product,status = 'Avialable',comments=transport.comments,sra=transport.sra)
        return created

    def createoutdoor(self,outdoor):
        asset,created = FixedAsset.objects.get_or_create(classification=outdoor.job_id.classification,description=outdoor.description,accountingrecognition=outdoor.accountingrecognition,depreciation=outdoor.depreciation,ipsascategory=outdoor.ipsascategory,subcategory=outdoor.subcategory,quantity=outdoor.quantity,ghanapostgpsaddress=outdoor.ghanapostgpsaddress,dateplacedinservice=outdoor.dateplacedinservice,
                        chassisno=outdoor.chassisno,engineserialno=outdoor.engineserialno,manufacturer=outdoor.manufacturer,model=outdoor.model,modelyear=outdoor.modelyear,tagno=outdoor.tagno,methodofacquisition=outdoor.methodofacquisition,currentstatus='Not in Use',conditions=outdoor.conditions,investmentproperty=outdoor.investmentproperty,fundsource=outdoor.fundsource,value=outdoor.value,usefullife=outdoor.usefullife,product=outdoor.product,status = 'Avialable',comments=outdoor.comments,sra=outdoor.sra)

    def createindoor(self,indoor):
        asset,created = FixedAsset.objects.get_or_create(classification=indoor.job_id.classification,description=indoor.description,accountingrecognition=indoor.accountingrecognition,depreciation=indoor.depreciation,ipsascategory=indoor.ipsascategory,subcategory=indoor.subcategory,quantity=indoor.quantity,dateplacedinservice=indoor.dateplacedinservice,chassisno=indoor.chassisno,manufacturer=indoor.manufacturer,tagno=indoor.tagno,methodofacquisition=indoor.methodofacquisition,currentstatus='Not in Use',conditions=indoor.conditions,investmentproperty=indoor.investmentproperty,fundsource=indoor.fundsource,value=indoor.value,
                        usefullife=indoor.usefullife,product=indoor.product,status = 'Avialable',comments=indoor.comments,sra=indoor.sra)
        return created

    def createwip(self,wip):
        asset,created = FixedAsset.objects.get_or_create(classification=wip.job_id.classification,description=wip.description,accountingrecognition=wip.accountingrecognition,depreciation=wip.depreciation,ipsascategory=wipipsascategory,quantity=wip.quantity,ghanapostgpsaddress=wip.ghanapostgpsaddress,commencement_date=wip.commencement_date,expectedcompletion_date=wip.expectedcompletion_date,accountingstatus=wip.accountingstatus,methodofacquisition=wip.methodofacquisition,fundsource=wip.fundsource,costbf=wip.costbf,currentperiodcost=wip.currentperiodcost,costcf=wip.costcf,product=wip.product,status = 'Avialable',comments=wip.comments)
        return created

    def run(self):
        print('started')
        try:
            for i in self.detail:
                if self.job.classification.name == 'Land':
                    land = i
                    fixedasset = self.createland(land)
                elif self.job.classification.name == 'Buldings And Other Structures':
                    building = i
                    fixedasset = self.createbuilding(building)
                elif self.job.classification.name == 'Transport Equipments':
                    transport = i
                    fixedasset = self.createtransport(transport)
                elif self.job.classification.name == 'Outdoor Machinery And Equipments':
                    outdoor = i
                    fixedasset = self.createoutdoor(outdoor)
                elif self.job.classification.name == 'Indoor':
                    indoor = i
                    fixedasset = self.createindoor(indoor)
                else:
                    wip = i
                    fixedasset = self.createwip(wip)
                print(fixedasset)
                if fixedasset:
                    inventory,created = Inventory.objects.get_or_create(product_id=i.product,tenant_id = self.user.devision.tenant_id)
                    inventory.avialable_quantity += 1
                    inventory.save()
        except IOError:
            print('fail')
            pass      