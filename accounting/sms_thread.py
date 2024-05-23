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
from  .utils import *



class  NotificationThread(threading.Thread):
    def __init__(self,item):
        self.pv = item
        self.recommmend_users = User.objects.filter(sub_division=self.pv.sub_division.id)
        self.office = 'Account'
        self.internal_audit_users = User.objects.filter(sub_division__name='Internal Audit')
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        for u in self.recommmend_users:
            if u.has_perm('accounting.custom_authorise_pv') and self.pv.status == 'Pending':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\nPayment Voucher with ID' + ' '+ str(self.pv.id) + ' '+ 'has been brought to you for recommendation.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Payment Voucher Voucher Recomendation For Approval"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass
            elif u.has_perm('accounting.custom_approve_pv') and self.pv.status == 'Authorised':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\nPayment Voucher with ID' + ' '+ str(self.pv.id) + ' '+ 'has been brought to you for approval.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Payment Voucher Approval"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass

            elif u.has_perm('accounting.custom_approve_pv') and self.pv.status == 'Paid':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\nPayment Voucher with ID' + ' '+ str(self.pv.id) + ' '+ 'has been paid.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Payment Voucher Paid"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass


            elif u.has_perm('accounting.custom_add_cheque_no') and self.pv.status == 'Authorised & Passed':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\nPayment Voucher with ID' + ' '+ str(self.pv.id) + ' '+ 'has been brought to you to enter Cheque number.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Payment Voucher Cheque Number"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to,fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass

            elif u.has_perm('accounting.custom_pay_pv') and self.pv.status == 'Check No Entered':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\nPayment Voucher with ID' + ' '+ str(self.pv.id) + ' '+ 'has been brought to you for payment.'
                phone = '233'+u.phone_number

                
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
               
                
                try:
                    subject = "Payment of Pv"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass
            
            elif u.has_perm('accounting.custom_create_pv') and self.pv.status == 'Returned':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\nPayment Voucher with ID' + ' '+ str(self.pv.id) + ' '+ 'has been returned by Internal Audit for Correction.'
                phone = '233'+u.phone_number

                
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
               
                
                try:
                    subject = "Payment of Pv"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass
            else:
                pass

class  AuditNotificationThread(threading.Thread):
    def __init__(self,item):
        self.pv = item
        print(self.pv.sub_division)
        if self.pv.sub_division.name == 'Accounts':
            self.internal_audit_users = User.objects.filter(sub_division__name = 'Internal Audit')
        else:
            self.internal_audit_users = User.objects.filter(sub_division=self.pv.sub_division.id)

        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        for u in self.internal_audit_users:
            if u.has_perm('accounting.custom_authorise_annd_pass_pv') and self.pv.status == 'Approved':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\nPayment Voucher with ID' + ' '+ str(self.pv.id) + ' '+ 'has been brought to your attention to check For Eligibility.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Payment Voucher Check For Eligibility"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass
            else:
                pass   

class  PayeeNotificationThread(threading.Thread):
    def __init__(self,item,code):
        self.pv = item
        self.code =code
        self.beneficiary = PaymentVoucherBeneficiary.objects.filter(pv_id=item.id)
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        
        if self.pv.status == 'Payee Notified':
            if self.pv.document.staff_through:
                usermessage =  'Dear ' + self.pv.document.staff_through.first_name +' ' + self.pv.document.staff_through.last_name  +','+'\nFunds for document with title' + ' '+ self.pv.document.title + ' '+ "is ready for payment. Please pass by Pay master's office for collection.You will be required to provide the funds release code blow"+'\n\nFUNDS RELEASE CODE: '+ str(self.code)
                phone = '233'+self.pv.document.staff_through.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                try:
                    subject = "Funds For Payment Ready"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [self.pv.document.staff_through.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass
            else:
                usermessage =  'Dear ' + self.pv.document.staff_from.first_name +' ' + self.pv.document.staff_from.last_name  +','+'\nFunds for document with title' + ' '+ self.pv.document.title + ' '+ "is ready for payment. Please pass by Pay master's office for collection.You will be required to provide the funds release code blow"+'\n\nFUNDS RELEASE CODE: '+ str(self.code)
                phone = '233'+self.pv.document.staff_from.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                try:
                    subject = "Funds For Payment Ready"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [self.pv.document.staff_from.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass
        
            if self.pv.status == 'Paid':
                if self.pv.document.staff_through:
                    usermessage =  'Dear ' + self.pv.document.staff_through.first_name +' ' + self.pv.document.staff_through.last_name  +','+'\nFunds for document with title' + ' '+ self.pv.document.title + ' '+ "has been paid"
                phone = '233'+self.pv.document.staff_through.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                try:
                    subject = "Funds For Payment Ready"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [self.pv.document.staff_through.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass
            else:
                usermessage =  'Dear ' + self.pv.document.staff_from.first_name +' ' + self.pv.document.staff_from.last_name  +','+'\nFunds for document with title' + ' '+ self.pv.document.title + ' '+ "has been paid"
                phone = '233'+self.pv.document.staff_from.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                try:
                    subject = "Funds For Payment Ready"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [self.pv.document.staff_from.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass


class  IndividualNotification(threading.Thread):
    def __init__(self,item):
        self.pv = item
        self.beneficiary = PaymentVoucherBeneficiary.objects.filter(pv_id=item.id)
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        
        for i in self.beneficiary:
            code = random_with_N_digits(6)
            i.code = code
            i.save()
            if self.pv.document:
                usermessage =  'Dear ' + i.staff.first_name +' ' + i.staff.last_name  +','+'\nFunds for document with title' + ' '+ self.pv.document.title + ' '+ "is ready for payment. Please pass by Pay master's office for collection.You will be required to provide the funds release code blow"+'\n\nFUNDS RELEASE CODE: '+ str(code)
            else:
                usermessage =  'Dear ' + i.staff.first_name +' ' + i.staff.last_name  +','+'\nFunds for document with title' + ' '+ self.pv.description + ' '+ "is ready for payment. Please pass by Pay master's office for collection.You will be required to provide the funds release code blow"+'\n\nFUNDS RELEASE CODE: '+ str(code)
            phone = '233'+i.staff.phone_number
            try:
                response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                print(response.json())
            except IOError as e:
                print(e)
                pass
            try:
                subject = "Funds For Payment Ready"
                message = usermessage
                sender = EMAIL_HOST_USER
                to = [i.staff.email]
                send_mail(subject, message, sender, to, fail_silently=True)
                print('mail one success')
            except Exception as e:
                print(e)
                pass
           

class IndividualPaymentNotification(threading.Thread):
    def __init__(self,item,staff):
        self.pv = item
        self.staff = staff
        threading.Thread.__init__(self)
        

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id

        usermessage =  'Dear ' + self.staff.first_name +' ' + self.staff.last_name  +','+'\nFunds for document with title' + ' '+ self.pv.description + ' '+  "has been paid"
        phone = '233'+self.staff.phone_number
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        try:
            subject = "Payment of Funds"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.staff.email]
            send_mail(subject, message, sender, to, fail_silently=True)
            print('mail one success')
        except Exception as e:
            print(e)
            pass


class IndividualResendCodeNotification(threading.Thread):
    def __init__(self,item,staff,code):
        self.pv = item
        self.staff = staff
        self.code = code
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id

        usermessage =  'Dear ' + self.staff.first_name +' ' + self.staff.last_name  +','+'\nFunds for document with title' + ' '+ self.pv.description + ' '+ "is ready for payment. Please pass by Pay master's office for collection.You will be required to provide the funds release code blow"+'\n\nFUNDS RELEASE CODE: '+ str(self.code)
        phone = '233'+self.staff.phone_number
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        try:
            subject = "Payment of Funds"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.staff.email]
            send_mail(subject, message, sender, to, fail_silently=True)
            print('mail one success')
        except Exception as e:
            print(e)
            pass

class  AccountHodNotificationThread(threading.Thread):
    def __init__(self,item):
        self.pv = item
        self.recommmend_users = User.objects.filter(sub_division__name='Accounts')
        
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        for u in self.recommmend_users:
            if u.has_perm('accounting.custom_approve_pv'):
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\n Payment Voucher with ID' + ' '+ str(self.pv.id) + ' '+'has been Paid.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Payment Of Pv"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass
            

class  IprestNotificationThread(threading.Thread):
    def __init__(self,item):
        self.imprest = item
        self.recommmend_users = User.objects.filter(sub_division=self.imprest.raised_by.sub_division)
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        for u in self.recommmend_users:    
            if u.has_perm('accounting.custom_certify_imprest'):
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\n Imprest with description' + ' '+ self.imprest.claim_detail + ' '+'has been brought to you for approval.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Imprest Approval"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass

class  IprestApprovedNotificationThread(threading.Thread):
    def __init__(self,item):
        self.imprest = item
        if self.imprest.raised_by.sub_division.tag:
            self.recommmend_users = User.objects.filter(sub_division__name='Accounts')
        else:
            self.recommmend_users = User.objects.filter(sub_division=self.imprest.raised_by.sub_division)

        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        for u in self.recommmend_users: 
            if u.has_perm('accounting.custom_certify_imprest') and self.imprest.status == 'Approved':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\n Imprest with description' + ' '+ self.imprest.claim_detail+ ' '+'has been brought to you to certify.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Imprest Certification"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass

        usermessage =  'Dear ' + self.imprest.raised_by.first_name +' ' + self.imprest.raised_by.last_name  +','+'\n Imprest with description' + ' '+ self.imprest.claim_detail + ' '+'has been approved and sent for certification.'
        phone = '233'+self.imprest.raised_by.phone_number
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        
        try:
            subject = "Imprest Approved"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.imprest.raised_by.email]
            send_mail(subject, message, sender, to, fail_silently=True)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
        
        usermessage =  'Dear ' + self.imprest.approved_by.first_name +' ' + self.imprest.approved_by.last_name  +','+'\n Imprest with description' + ' '+ self.imprest.claim_detail + ' '+'has been approved and sent for certification.'
        phone = '233'+self.imprest.approved_by.phone_number
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        
        try:
            subject = "Imprest Approved"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.imprest.approved_by.email]
            send_mail(subject, message, sender, to, fail_silently=True)
            print('mail one success')
        except Exception as e:
            print(e)
            pass

class  IprestCertifiedNotificationThread(threading.Thread):
    def __init__(self,item):
        self.imprest = item
        if self.imprest.raised_by.sub_division.tag:
            self.recommmend_users = User.objects.filter(sub_division__name='Accounts')
        else:
            self.recommmend_users = User.objects.filter(sub_division=self.imprest.raised_by.sub_division)

        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        for u in self.recommmend_users:    
            if u.has_perm('accounting.custom_pay_imprest') and self.imprest.status == 'Certified':
                usermessage =  'Dear ' + u.first_name +' ' + u.last_name  +','+'\nImprest with description:' + ' '+ self.imprest.claim_detail+ ' '+'has been brought to you to pay.'
                phone = '233'+u.phone_number
                try:
                    response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                    print(response.json())
                except IOError as e:
                    print(e)
                    pass
                
                try:
                    subject = "Payment Of Imprest"
                    message = usermessage
                    sender = EMAIL_HOST_USER
                    to = [u.email]
                    send_mail(subject, message, sender, to, fail_silently=True)
                    print('mail one success')
                except Exception as e:
                    print(e)
                    pass

        usermessage =  'Dear ' + self.imprest.raised_by.first_name +' ' + u.last_name  +','+'\nImprest with description:' + ' '+ self.imprest.claim_detail + ' '+'has been certified and ready to be paid'
        phone = '233'+self.imprest.raised_by.phone_number
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        
        try:
            subject = "Payment Of Imprest"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.imprest.raised_by.email]
            send_mail(subject, message, sender, to, fail_silently=True)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
        
        usermessage =  'Dear ' + self.imprest.approved_by.first_name +' ' + u.last_name  +','+'\nImprest with description:' + ' '+ self.imprest.claim_detail + ' '+'has been certified and ready to be paid.'
        phone = '233'+self.imprest.approved_by.phone_number
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        
        try:
            subject = "Payment Of Imprest"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.imprest.approved_by.email]
            send_mail(subject, message, sender, to, fail_silently=True)
            print('mail one success')
        except Exception as e:
            print(e)
            pass


class  IprestPaymentNotificationThread(threading.Thread):
    def __init__(self,item):
        self.imprest = item
       
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        

        usermessage =  'Dear ' + self.imprest.raised_by.first_name +' ' + self.imprest.raised_by.last_name  +','+'\nImprest with description:' + ' '+ self.imprest.claim_detail + ' '+'has been paid.'
        phone = '233'+self.imprest.raised_by.phone_number
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        
        try:
            subject = "Payment Of Imprest"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.imprest.raised_by.email]
            send_mail(subject, message, sender, to, fail_silently=True)
            print('mail one success')
        except Exception as e:
            print(e)
            pass
        
        usermessage =  'Dear ' + self.imprest.approved_by.first_name +' ' + self.imprest.raised_by.last_name  +','+'\nImprest with description:' + ' '+ self.imprest.claim_detail + ' '+'has been paid.'
        phone = '233'+self.imprest.approved_by.phone_number
        try:
            response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
            print(response.json())
        except IOError as e:
            print(e)
            pass
        
        try:
            subject = "Payment Of Imprest"
            message = usermessage
            sender = EMAIL_HOST_USER
            to = [self.imprest.approved_by.email]
            send_mail(subject, message, sender, to, fail_silently=True)
            print('mail one success')
        except Exception as e:
            print(e)
            pass


class  ImpresthodNotificationThread(threading.Thread):
    def __init__(self,imprest):
        self.imprest = imprest
        self.hods = User.objects.filter(sub_division=self.imprest.raised_by.sub_division.id)
        threading.Thread.__init__(self)
    def run(self):
        print('started')
        url =endPoint + '&api_key=' + key 
        senders = Sender_Id
        if self.hods:
            for staff in self.hods:
                if staff.has_perm('accounting.custom_approve_imprest'):
                    usermessage =  'Dear ' + staff.first_name +' ' + staff.last_name  +','+'\nImprest with description:' + ' '+ self.imprest.claim_detail + ' '+'has been brought to your attention for approval.'
                    phone = '233'+staff.phone_number
                    try:
                        response = requests.get(url+'&to='+phone+'&from='+senders+'&sms='+usermessage)
                        print(response.json())
                    except IOError as e:
                        print(e)
                        pass
                
                    try:
                        subject = "Approval of Imprest"
                        message = usermessage
                        sender = EMAIL_HOST_USER
                        to = [staff.email]
                        send_mail(subject, message, sender, to, fail_silently=True)
                        print('mail one success')
                    except Exception as e:
                        print(e)
                        pass
        else:
            pass
        
        