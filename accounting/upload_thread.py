
import threading
from django.utils.datastructures import MultiValueDictKeyError
from .models import *
from authentication.models import User

class  CurrencyThread(threading.Thread):
    def __init__(self, dbframe):
        self.data = dbframe 
       
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                Currency.objects.get_or_create(name=i.Currency.title().strip(),symbol=i.Symbol.upper().strip(),rate=i.Rate)
        except IOError:
            print('fail')
            pass 

        

class  ChartOfAccountsThread(threading.Thread):
    def __init__(self, dbframe):
        self.data = dbframe 
       
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                try:
                   account_class= Account_Class.objects.get(code = i.AccountClassCode)
                except Account_Class.DoesNotExist:
                    account_class= Account_Class.objects.create(name=i.AccountClass.strip(),code = i.AccountClassCode)
                try:
                   account_item = AccountItem.objects.get(name=i.AccountItem.strip(),account_class_id__name=i.AccountClass)
                except AccountItem.DoesNotExist:
                    account_item = AccountItem.objects.create(name=i.AccountItem.strip(),code = i.AccountItemCode,account_class_id=account_class)
                try:
                   sub_item= AccountSubItem.objects.get(name=i.AccountSubItem.strip())
                except AccountSubItem.DoesNotExist:
                    sub_item = AccountSubItem.objects.create(name=i.AccountSubItem.strip(),code = i.AccountSubItemCode,account_item_id=account_item)

                AccountLedger.objects.get_or_create(name=i.AccountSubSubItem.strip(),account_number = i.AccountSubSubCode,code=i.Code,account_sub_item_id=sub_item)
        except IOError:
            print('fail')
            pass 

class  BanktypeThread(threading.Thread):
    def __init__(self, dbframe):
        self.data = dbframe 

        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:
            for i in self.data.itertuples():
                BankAccountsType.objects.get_or_create(name=i.BankAccountsType.title().strip())
        except IOError:
            print('fail')
            pass