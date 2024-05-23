from __future__ import absolute_import, unicode_literals
from celery import shared_task
from erpproject.settings import  endPoint,key,Sender_Id, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import requests
from authentication.models import User
from django.contrib.auth import get_user_model



@shared_task(bind=True)
def low_stock_alert(self):
    
    companys = Tenants.objects.all()
    url = endPoint + '&api_key=' + key
     
    for i in companys:
        products = Inventory.objects.filter(tenant_id=i.id,avialable_quantity__lte = F('product_id__restock_level'))
        item =[]
        for product in products:
            print(product.product_id.name)
            item.append(product.product_id)
        print(item)
        user = User.objects.filter(tenant_id=i.id)
        for u in user:
            if u.has_perm('authentication.custom_view_report'):
                body = [
                    
                    'Dear' + ' '+u.first_name + ' '+ u.last_name + ', ' +'the following product are running low on stock'
                    
                    '\n\nLow on Stock Summery :\n------------------------',
                    '\n'.join(item),
                    '\nThank you for using Smart ERP',
                    ]
                m = body
                message =  "\n".join(m)
                print(message)
                phone='233'+u.phone_number
                senders = Sender_Id
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+message)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
    
    return "Done"

# @shared_task(bind=True)
# def send_sms_hod(self,first_name,last_name,devision,phone,ids):
#     hod = User.objects.filter(sub_division=devision)
#     print(devision)
#     url =endPoint + '&api_key=' + key 
#     senders = Sender_Id
    
#     usermessage =  'Dear ' + last_name +' ' +first_name  +','+'\nYour requisition with batch number' + ' '+ str(ids) + ' '+ 'has been sent for approval. You will be notified when it is ready.'
#     phone = '233'+phone

#     try:
#         response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
#         print(response.json())
#     except IOError as e:
#         print(e)
#         pass
    
#     # hod = User.objects.filter(sub_division=devision)
#     for i in hod:
#         if i.has_perm('inventory.custom_approve_requisition'):
#             message = 'Dear ' + i.first_name + ' '+ i.last_name +',' + '\nRequisition with batch number' + ' '+ str(ids) + ' '+ 'has been brougth to you attention for approval.'
#             try:
#                 response = requests.get(url+'&to='+'233'+i.phone_number+'&from='+senders+'&sms='+message)
#                 print(response.json())
#             except IOError as e:
#                 print(e)
#                 pass
    
#     return "Done"
