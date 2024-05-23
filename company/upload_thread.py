
import threading
from django.utils.datastructures import MultiValueDictKeyError
from .models import *
from authentication.models import User
from fixedassets.models import Location

class  DevisionThread(threading.Thread):
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
                Devision.objects.get_or_create(name=i.CostCenter.title().strip(),code=i.Code,tenant_id=tenant)
        except IOError:
            print('fail')
            pass


class  Sub_DevisionThread(threading.Thread):
    def __init__(self, dbframe):
        self.data = dbframe 
       
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                try:
                    devision = Devision.objects.get(name=i.CostCenter.title().strip())
                except Devision.DoesNotExist:
                    devision= Devision.objects.create(name=i.CostCenter.title().strip())
                try:
                    location = Location.objects.get(location=i.Location.title().strip())
                except Location.DoesNotExist:
                    location= Location.objects.create(location=i.Location.title().strip())
                district,created = Sub_Devision.objects.get_or_create(name=i.SubCostCenter.title().strip(),code=i.Code,devision=devision)
                district.location = location
                district.save()
        except IOError:
            print('fail')
            pass

class  ApprovalThread(threading.Thread):
    def __init__(self, dbframe):
        self.data = dbframe 
       
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                
                tenant= Tenants.objects.get(name=i.Institutuion.title().strip())
                user =User.objects.get(staffid = i.Staffid,tenant_id=tenant)
                approval = Approvals.objects.get_or_create(tenant_id=tenant,user_id=user,classification=i.Classification.title().strip(),type_of_approval=i.ApprovalType.title().strip())
               
        except IOError:
            print('fail')
            pass
