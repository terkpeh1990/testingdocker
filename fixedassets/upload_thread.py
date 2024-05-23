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
 
class  DataUploadThread(threading.Thread):
    def __init__(self, dbframe,action):
        self.data = dbframe 
        self.action = action
       
        threading.Thread.__init__(self)

    def clasification(self,name):
       classification,created = Classification.objects.get_or_create(name=name)
       return classification
    
    def recognition(self,recognition,classification):
        AccountingRecognition.objects.get_or_create(name=recognition,classification = classification)

    def gfscategory(self,code,name):
        gfscategory,created =GFSCategory.objects.get_or_create(code=code,name=name)
        return gfscategory

    def ipsascategory(self,category,classification,gfscategory):
        ipsascategory = IPSASCategory.objects.get_or_create(name=category,classification = classification,gfscategory=gfscategory)
        
    def getipsascategory(self,category,classification):
        ipsascategory = IPSASCategory.objects.get(name=category,classification=classification)
        return ipsascategory
    
    def subcategory(self,category,classification,ipsascategory):
        SubCategory.objects.get_or_create(name=category,classification = classification,gfscategory=gfscategory)
        

    def location(self,location,code):
        Location.objects.get_or_create(location=location,code = code)

    def funding(self,code,funding):
        SourceOfFunding.objects.get_or_create(code=code,funding=funding)
    
    def subcategory(self,subcategory,ipsascategory):
        SubCategory.objects.get_or_create(name=subcategory,ipsascategory=ipsascategory)

    def methodofacquisition(self,name):
        MothodofAcquisition.objects.get_or_create(name=name)


    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                if self.action == 'classification':
                    name = i.Classification.title().strip()
                    self.clasification(name)

                elif self.action == 'recognition':
                    name = i.Classification.title().strip()
                    classification= self.clasification(name)
                    recognition = i.AccountingRecognition.title().strip()
                    self.recognition(recognition,classification)
                
                elif self.action == 'ipsascategory':
                    name = i.Classification.title().strip()
                    classification= self.clasification(name)
                    gfscode = i.GFSCategoryCode
                    gfsname = i.GFSCategoryName.title().strip()
                    gfscategory = self.gfscategory(code=gfscode,name=gfsname)
                    category = i.IPSASCategory.title().strip()
                    category = self.ipsascategory(category,classification,gfscategory)

                elif self.action == 'location':
                    location = i.Location.title().strip()
                    code = i.Code
                    self.location(location,code)
                
                elif self.action == 'funding':
                    code = i.Code
                    funding = i.Funding
                    self.funding(code,funding)
                elif self.action == 'gfscategory':
                    code = i.GFSCategoryCode
                    name = i.GFSCategoryName.title().strip()
                    self.gfscategory(code,name)

                elif self.action == 'subcategory':
                    subcategory= i.SubCategory.title().strip()
                    category = i.IPSASCategory.title().strip()
                    name = i.Classification.title().strip()
                    classification= self.clasification(name)
                    print(category)
                    ipsascategory = self.getipsascategory(category,classification)
                    aa=self.subcategory(subcategory,ipsascategory)
                    print(aa)

                elif self.action == 'methodofacquisition':
                    name= i.Methodofacquisition
                    self.methodofacquisition(name)


                else:
                    pass
        except IOError:
            print('fail')
            pass


class  DepreciationThread(threading.Thread):
    def __init__(self, depreciation,assets):
        self.depreciation = depreciation 
        self.assets= assets
        threading.Thread.__init__(self)

    def calculatedepreciation(self,value,usefullife):
       currentdepreciation = (value/usefullife)
       return currentdepreciation
    
    def recorddepreciation(self,dep,asset,depreciationvalue):
        depreciateditem,created= DepreciationDetail.objects.get_or_create(depreciation=dep,asset=asset,depreciationvalue=depreciationvalue)
    
    def run(self):
        print('started')
        try:
            for i in self.assets:
                value = float(i.value)
                usefullife = float(i.usefullife)
                asset = i
                depreciationvalue = self.calculatedepreciation(value,usefullife)
                decimaldepreciatedvalue = Decimal(depreciationvalue)
                asset.currentdepreciation = decimaldepreciatedvalue
                asset.accumulateddepreciation += decimaldepreciatedvalue
                asset.depreciatedlife +=1
                dep = self.depreciation
                self.recorddepreciation(dep,asset,depreciationvalue)
                asset.save()
                self.depreciation.depreciationvalue+=depreciationvalue
                self.depreciation.save()
            self.depreciation.status = 'Completed'
            self.depreciation.save()
        except IOError:
            print('fail')
            pass

