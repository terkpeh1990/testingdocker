from django.db import models
from company.models import *
from authentication.models import *
from django.conf import settings
# from accounting.models import Currency
from .validators import validate_file_extension
from inventory.models import Supplier
from decimal import Decimal
from inventory.models import Products
from django.core.validators import RegexValidator

class DocumentCategory(models.Model):
    name = models.CharField(max_length=250)
    can_delete = models.BooleanField(default=False)
    pin_down = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'documentowner', null=True, blank=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'documentcategory',on_delete=models.CASCADE)

    class Meta:
        db_table = 'DocumentCategorys'
        verbose_name = 'DocumentCategory'
        verbose_name_plural = 'DocumentCategorys'

    def __str__(self):
        return f"{self.name}"

class Document(models.Model):
    types = (
        ('Memo','Memo'),
        ('Application','Application'),
        ('Others','Others'),
    )
   
    type_of_document = models.CharField(max_length=50, choices=types, null=True, blank=True)
    title = models.CharField(max_length=250)
    document_date = models.DateField(null=True, blank=True)
    staff_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'to_staff', null=True, blank=True)
    document_to = models.CharField(max_length=250,blank=True, null=True)
    document_to_grade = models.CharField(max_length=250,blank=True, null=True)
    staff_from = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'from_staff', null=True, blank=True)
    document_from = models.CharField(max_length=250,blank=True, null=True)
    document_from_grade = models.CharField(max_length=250,blank=True, null=True)
    staff_through = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'through_staff', null=True, blank=True)
    document_through = models.CharField(max_length=250,blank=True, null=True)
    document_through_grade = models.CharField(max_length=250,blank=True, null=True)
    status = models.BooleanField(default = False)
    reverse = models.BooleanField(default = False)
    sub_division  = models.ForeignKey(Sub_Devision, blank=True, null=True,on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,related_name = 'supplier', null=True, blank=True)
    currency_id = models.ForeignKey(
        'accounting.Currency', blank=True, null=True, related_name = 'dcurrency',on_delete=models.CASCADE)
    approved_budget = models.DecimalField(max_digits=10, decimal_places=2,default=1.00)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'document',on_delete=models.CASCADE)

    class Meta:
        db_table = 'Documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
    
        permissions = [
            ("custom_create_document", "Can Create Document"),
            ("custom_delete_document", "Can Delete Document"),
            ("custom_delete_change_status", "Can Change Status of Document"),
            ("custom_create_document_for", "Can Create Document For"),
            ("custom_can_approve_document", "Can Approve Document"),
            ("custom_can_create_pv_from_document", "Can Create Pv From Approved Budget"),
            ("custom_can_add_approve_budget_amount", "Can Add Approved Budget"),
            ("custom_can_add_supplier", "Can Add Supplier"),
            ("custom_can_notify_procurement", "Can Notify Procurement"),
            
        ]

    def __str__(self):
        return f"{self.title} --- {self.tenant_id.name}"

class DocumentDestination(models.Model):
    status= (
        ('Draft','Draft'),
        ('Wait To Send','Wait To Send'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Inbound','Inbound'),
        ('Outbound','Outbound'),
        ('Returned','Returned'),
        ('Cancelled','Cancelled'),  
        ('Pv Created','Pv Created'),  
    )
    document_id = models.ForeignKey(
        Document, blank=True, null=True, related_name = 'documentassignedment',on_delete=models.CASCADE)
    category_id = models.ForeignKey(
        DocumentCategory, blank=True, null=True, related_name = 'documentcategory',on_delete=models.CASCADE)
    minutes = models.CharField(max_length=255, null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, choices= status,blank=True, null=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'documentdestination',on_delete=models.CASCADE)
    class Meta:
        db_table = 'DocumentDestinations'
        verbose_name = 'DocumentDestination'
        verbose_name_plural = 'DocumentDestinations'

    def __str__(self):
        return f"{self.document_id.title} --- {self.document_id.tenant_id.name}"   

class DocumentDetails(models.Model):
    document_id = models.ForeignKey(
        Document, blank=True, null=True, related_name = 'documentdetail',on_delete=models.CASCADE)
    paragraph = models.CharField(max_length=1200)
    destination = models.ForeignKey(
        DocumentDestination, blank=True, null=True, related_name = 'documentdestination',on_delete=models.CASCADE)

    class Meta:
        db_table = 'DocumentDetails'
        verbose_name = 'DocumentDetail'
        verbose_name_plural = 'DocumentDetails'

    def __str__(self):
        return self.paragraph
    
class DocumentBudget(models.Model):
    document_id = models.ForeignKey(
        Document, blank=True, null=True, related_name = 'documentbudget',on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    attachment=models.FileField(upload_to='documents/%Y/%m/%d/',validators=[validate_file_extension],blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    destination = models.ForeignKey(
        DocumentDestination, blank=True, null=True, related_name = 'documentbudgetdestination',on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'DocumentBudgets'
        verbose_name = 'DocumentBudget'
        verbose_name_plural = 'DocumentBudgets'

    def __str__(self):
        return self.paragraph
    
  
    


    
class Documenttimeline(models.Model):
    document_id = models.ForeignKey(
        Document, blank=True, null=True, related_name = 'documenttimeline',on_delete=models.CASCADE)
    minutes = models.CharField(max_length=255, null=True, blank=True)
    timeline_comment = models.CharField(max_length=255, null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timelinedate = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Documenttimelines'
        verbose_name = 'Documenttimeline'
        verbose_name_plural = 'Documenttimelines'

    def __str__(self):
        return f"{self.document_id.title} --- {self.timeline_comment}"



class Documentattachement(models.Model):
    document_id = models.ForeignKey(
        Document, blank=True, null=True, related_name = 'attachment',on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    attachment=models.FileField(upload_to='documents/%Y/%m/%d/',validators=[validate_file_extension])
    destination = models.ForeignKey(
        DocumentDestination, blank=True, null=True, related_name = 'documentattachmentdestination',on_delete=models.CASCADE)
    
    class Meta:
        db_table = ' Documentattachements'
        verbose_name = ' Documentattachement'
        verbose_name_plural = ' Documentattachement'

    def __str__(self):
        return f"{self.document_id.title} --- {self.timeline_comment}"


class DocumentBeneficiary(models.Model):
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 

     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    document_id = models.ForeignKey(
        Document, blank=True, null=True, related_name = 'documentbeneficiary',on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20,validators=[phone_regex],null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_received = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default = False)
    
    class Meta:
        db_table = 'DocumentBeneficiaries'
        verbose_name = 'DocumentBeneficiary'
        verbose_name_plural = 'DocumentBeneficiaries'

    def __str__(self):
        return f"{self.document_id.title} --- {self.name} --- {self.amount}"
    
    def save(self, *args, **kwargs):
        self.balance = self.amount -  Decimal(self.amount_received)
        super(DocumentBeneficiary, self).save(*args, **kwargs)

class DocumentProducts(models.Model):
    document_id = models.ForeignKey(
        Document, blank=True, null=True, related_name = 'documentproduct',on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,related_name='document_productslist', on_delete= models.CASCADE)
    status = models.BooleanField(default = False)

    class Meta:
        db_table = 'DocumentProducts'
        verbose_name = 'DocumentProducts'
        verbose_name_plural = 'DocumentProductss'

    def __str__(self):
        return f"{self.document_id.title} --- {self.product_id.name}"
    