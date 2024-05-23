from django.db import models
from .utils import *
from company.models import *
from django.core.validators import RegexValidator
from authentication.models import *
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone
# from fixedassets.models import *
 


class Unit_of_Measurement(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'unit',on_delete=models.CASCADE)
   
    class Meta:
        
        db_table = 'Measurements'
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'

        permissions = [
            ("custom_create_measuremnt", "Can Create Measurement"),
            ("custom_update_measuremnt", "Can Update Measurement"),
            ("custom_delete_measuremnt", "Can Delete Measurement"),
            ("custom_view_measuremnt", "Can View Measurement"),
        ]

    def __str__(self):
        return f"{self.name} ---- {self.tenant_id}"

class Categorys(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)
    description = models.CharField(max_length=250,null=True,blank=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'categories',on_delete=models.CASCADE)
   
    class Meta:
        
        db_table = 'Categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

        permissions = [
            ("custom_create_category", "Can Create Category"),
            ("custom_update_category", "Can Update Category"),
            ("custom_delete_category", "Can Delete Category"),
            ("custom_view_category", "Can View Category"),
        ]

    def __str__(self):
        return f"{self.name} ---- {self.tenant_id}"

class Brands(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'brand',on_delete=models.CASCADE)
    class Meta:
        
        db_table = 'Brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

        permissions = [
            ("custom_create_brand", "Can Create Brand"),
            ("custom_update_brand", "Can Update Brand"),
            ("custom_delete_brand", "Can Delete Brand"),
            ("custom_view_brand", "Can View Brand"),
            
        ]

    def __str__(self):
        return f"{self.name} ---- {self.tenant_id}"


class Products(models.Model):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
         
    )
    category_id =models.ForeignKey(Categorys,related_name = 'products', on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=250,null=True, blank=True)
    restock_level = models.PositiveIntegerField(default=0)
    unit_of_measurement =models.ForeignKey(Unit_of_Measurement, on_delete=models.CASCADE,null=True, blank=True) 
    type_of_product = models.CharField(max_length=50, choices= sts,blank=True, null=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'products',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


    class Meta:
        db_table = 'Products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

        permissions = [
            ("custom_create_product", "Can Create Product"),
            ("custom_update_product", "Can Update Product"),
            ("custom_delete_rproduct", "Can Delete Product"),
            ("custom_view_product", "Can View Product"),
        ]

    def __str__(self):
        return f"{self.name} ---- {self.tenant_id}"


class Inventory(models.Model):
    product_id =models.ForeignKey(Products,related_name ='inventory' ,on_delete=models.CASCADE,null=True, blank=True)
    avialable_quantity = models.PositiveIntegerField(default=0)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'tenant_inventory',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    
    def __str__(self):
        return str(self.id)



class Inventory_Details(models.Model):
    inventory_id =models.ForeignKey(Inventory,related_name ='inventory_details', on_delete=models.CASCADE,null=True, blank=True)
    quantity_intake = models.PositiveIntegerField(default=0)
    quantity_requested = models.PositiveIntegerField(default=0)
    avialable_quantity = models.PositiveIntegerField(default=0)
    batch_number =  models.CharField(max_length=250)
    date_received = models.DateField(auto_now_add=True)
    expiring_date  = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['expiring_date']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.avialable_quantity = self.quantity_intake - self.quantity_requested
        super(Inventory_Details, self).save(*args, **kwargs)


class Supplier(models.Model):
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 

     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    name = models.CharField(max_length=250,null=True,blank=True)
    phone_number = models.CharField(max_length=20,validators=[phone_regex],null=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)
    country = models.CharField(max_length=250,null=True,blank=True)
    phone_number = models.CharField(max_length=20,validators=[phone_regex],null=True)
    supplier_email = models.CharField(max_length=250,null=True,blank=True)
    
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'supplier',on_delete=models.CASCADE)
    class Meta:
        
        db_table = 'Supplier'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

        permissions = [
            ("custom_create_supplier", "Can Create Supplier"),
            ("custom_update_supplier", "Can Update Supplier"),
            ("custom_delete_supplier", "Can Delete Supplier"),
            ("custom_view_supplier", "Can View Supplier"),
            
        ]

    def __str__(self):
        return f"{self.name} ---- {self.tenant_id}"

class Supplier_Products(models.Model):
    product_id =models.ForeignKey(Products,related_name ='suppliers_product' ,on_delete=models.CASCADE,null=True, blank=True)
    supplier_id = models.ForeignKey(
        Supplier, blank=True, null=True, related_name = 'supplies',on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        
        db_table = 'Suppliers_Product'
        verbose_name = 'Suppliers_Product'
        verbose_name_plural = 'Suppliers_Products'
    

class Restocks(models.Model):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
         
    )
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 

     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    status = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )
    restock_date =  models.DateTimeField()
    supplier_id = models.ForeignKey(
        Supplier, blank=True, null=True, related_name = 'restock',on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=250,null=True,blank=True)
    driver_contact =models.CharField(max_length=250,validators=[phone_regex],null=True,blank=True)
    status = models.CharField(
        max_length=10, choices=status, default='Pending')
    classification = models.CharField(max_length=50, choices= sts,default="Consumables",blank=True, null=True)
   
    note  = models.CharField(max_length=1200, null=True, blank=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'restock',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        
        db_table = 'Restock'
        verbose_name = 'Restock'
        verbose_name_plural = 'Restocks'

        permissions = [
            ("custom_create_restock", "Can Create Restock"),
            ("custom_update_restock", "Can Update Restock"),
            ("custom_delete_restock", "Can Delete Restock"),
            ("custom_view_restock", "Can View Restock"),
           
            
        ]

class Restock_details(models.Model):
    restock_id =models.ForeignKey(Restocks, blank=True, related_name = 'details',on_delete=models.CASCADE,null=True)
    product_id =models.ForeignKey(Products, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    expiring_date =models.DateField(null=True)
    batch_number = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.product_id.name

    def save(self, *args, **kwargs):
        if not self.batch_number:
            number = incrementor()
            self.batch_number = number()
            while Restock_details.objects.filter(batch_number=self.batch_number).exists():
                self.batch_number = number()
        super(Restock_details, self).save(*args, **kwargs)

    class Meta:
        
        db_table = 'Restock_detail'
        verbose_name = 'Restock_detail'
        verbose_name_plural = 'Restock_details'

        

class Job_Certification(models.Model):
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 

     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    status = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )
    certification_date =  models.DateTimeField()
    supplier_id = models.ForeignKey(
        Supplier, blank=True, null=True, related_name = 'jobcert',on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=status, default='Pending')
    quantity = models.PositiveIntegerField(default=0)
    quantity_accepted = models.PositiveIntegerField(default=0)
    quantity_rejected = models.PositiveIntegerField(default=0)
    note  = models.CharField(max_length=1200, null=True, blank=True)
    classification = models.ForeignKey('fixedassets.Classification', related_name='jobclassification', on_delete=models.CASCADE,null=True)
    category =models.ForeignKey(Categorys,related_name = 'jobcategory', on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey('inventory.Products', related_name='jobproduct', on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=255,null=True)
    sra = models.CharField(max_length=255,null=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'job',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        
        db_table = 'JobCertification'
        verbose_name = 'JobCertification'
        verbose_name_plural = 'JobCertifications'

        permissions = [
            ("custom_create_job_certification", "Can Create Job Certification"),
            ("custom_update_job_certification", "Can Update Job Certification"),
            ("custom_delete_job_certification", "Can Delete Job Certification"),
            ("custom_view_job_certification", "Can View Job Certification"),
            
        ]

       
class Job_detail(models.Model):
    status = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
       
    )
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usage = (
        ('Public Domain', 'Public Domain'),
        ('Private Domain', 'Private Domain'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    
    st = (
        
        ('Assigned', 'Assigned'),
        ('Avialable', 'Avialable'),
    )
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    bcondition = (
        ('Good','Good'),
        ('Needs Repair/Renovation/Servicing','Needs Repair/Renovation/Servicing'),
        ('Irrepairable/Unserviceable','Irrepairable/Unserviceable'),
        ('Not Sighted','Not Sighted'),
    )
    accountingstatus = (
        ('In-progress','In-progress'),
        ('Completed','Completed'),
        ('Completed and Transferred','Completed and Transferred'),
       
    )

    job_id =models.ForeignKey(Job_Certification, on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=255,null=True)
    registrationnumber = models.CharField(max_length=255,null=True,unique=True, error_messages={'unique':"Vehicle With this Registration number already exist."})
    accountingrecognition = models.ForeignKey('fixedassets.AccountingRecognition', related_name='jobaccountingrecognition', on_delete=models.CASCADE,null=True)
    depreciation = models.CharField(max_length=4,choices=condition,null=True)
    amotization = models.CharField(max_length=4, choices=condition, null=True)
    usage = models.CharField(max_length=17, choices=usage, null=True)
    ipsascategory  = models.ForeignKey('fixedassets.IPSASCategory', related_name='jobipsascategory', on_delete=models.CASCADE,null=True)
    subcategory  = models.ForeignKey('fixedassets.SubCategory', related_name='jobsubcategory', on_delete=models.CASCADE,null=True)
    gfscategory  = models.ForeignKey('fixedassets.GFSCategory', related_name='jobgfscategory', on_delete=models.CASCADE,null=True)
    size =  models.CharField(max_length=255,null=True)
    quantity =models.PositiveIntegerField(default=1,null=True)
    location  = models.ForeignKey('fixedassets.Location', related_name='jobassetlocation', on_delete=models.CASCADE,null=True)
    usagetype = models.CharField(max_length=10,choices=usagetype,null=True)
    ghanapostgpsaddress = models.CharField(max_length=255,null=True)
    dateplacedinservice = models.DateField(null=True)
    colour = models.CharField(max_length=255,null=True)
    chassisno = models.CharField(max_length=255,null=True,unique=True, error_messages={'unique':"Asset With this Chassis/Serial number already exist."})
    tagno = models.CharField(max_length=255,null=True,unique=True, error_messages={'unique':"Asset With this Chassis/Serial number already exist."})
    engineserialno = models.CharField(max_length=255,null=True,unique=True, error_messages={'unique':"Asset With this Tag number already exist."})
    manufacturer = models.ForeignKey('Brands', related_name='jobmanufacturername', on_delete=models.CASCADE,null=True)
    model = models.CharField(max_length=255,null=True)
    modelyear = models.IntegerField(null=True)
    costcenter = models.ForeignKey('company.Devision', related_name='jobassetcostcenter', on_delete=models.CASCADE,null=True)
    subcostcenter = models.name = models.ForeignKey('company.Sub_Devision', related_name='jobassetsubcostcenter', on_delete=models.CASCADE,null=True)
    titled = models.CharField(max_length=4, choices=condition, null=True)
    staffid = models.CharField(max_length=255,null=True)
    fullname = models.CharField(max_length=255,null=True)
    position = models.name = models.ForeignKey('authentication.Grade', related_name='jobposition', on_delete=models.CASCADE,null=True)
    methodofacquisition  = models.ForeignKey('fixedassets.MothodofAcquisition', related_name='jobassetmethodofacquisition', on_delete=models.CASCADE,null=True)
    conditions = models.CharField(max_length=40,choices=bcondition,null=True)
    investmentproperty = models.CharField(max_length=4,choices=condition,null=True)
    fundsource = models.ForeignKey('fixedassets.SourceOfFunding', related_name='jobassetfundsource', on_delete=models.CASCADE,null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    usefullife = models.PositiveIntegerField(default=0,null=True) 
    desposal_date = models.DateField(null=True)
    methodofdesposal = models.CharField(max_length=50,choices=disposal,null=True)
    proceedsfromsales = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    commencement_date = models.DateField(null=True)
    expectedcompletion_date = models.DateField(null=True)
    accountingstatus = models.CharField(max_length=50,choices=accountingstatus,null=True)
    costbf = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    currentperiodcost = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    costcf = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    comments = models.CharField(max_length=255,null=True)
    accumulateddepreciation = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    currentdepreciation = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    totaldepreciation = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    netbookvalue = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    user = models.ForeignKey('authentication.User', related_name='jobcurrentuser', on_delete=models.CASCADE,null=True)
    product = models.ForeignKey('Products', related_name='jobfixedassetproduct', on_delete=models.CASCADE,null=True)
    depreciatedlife  = models.PositiveIntegerField(default=0,null=True)
    usefullifebalance = models.PositiveIntegerField(default=0,null=True)
    status = models.CharField(max_length=10, choices=status)
    

    def __str__(self):
        return self.product_id.name

    class Meta:
        
        db_table = 'Job_detail'
        verbose_name = 'Job_detail'
        verbose_name_plural = 'Job_details'
    
    def save(self, *args, **kwargs):
           
        if not self.tagno:
            number = incrementor()
            self.tagno = number()
            while Job_detail.objects.filter(tagno=self.tagno).exists():
                self.id = number()
        super(Job_detail, self).save( *args, **kwargs)


class Assets(models.Model):  
    product_id =models.ForeignKey(Products, on_delete=models.CASCADE,null=True)
    serial_number = models.CharField(max_length=250,null=True,blank=True)
    description = models.CharField(max_length=250,null=True,blank=True)
    status = models.BooleanField(default=False)
    brand_id =models.ForeignKey(Brands, on_delete=models.CASCADE,null=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'assets',on_delete=models.CASCADE)
    def __str__(self):
        return self.product_id.name
    
    class Meta:
        
        db_table = 'Asset'
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'


class Requisition(models.Model):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
         
    )
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Awaiting Approval','Awaiting Approval'),
        ('Issued','Issued'),
        ('Cancelled','Cancelled'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    requisition_date = models.DateField(null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=stat, default="Pending", null=True, blank=True)
    classification = models.CharField(max_length=60, choices=sts, null=True, blank=True)
    devision  = models.ForeignKey(Devision, blank=True, null=True, related_name = 'reqdevisions',on_delete=models.CASCADE)
    sub_division  = models.ForeignKey(Sub_Devision, blank=True, null=True, related_name = 'reqsub_districts',on_delete=models.CASCADE)
    release = models.BooleanField(default=False)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'req',on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.id

    class Meta:
        
        db_table = 'Requisition'
        verbose_name = 'Requisition'
        verbose_name_plural = 'Requisitions'

        permissions = [
            ("custom_create_requisition", "Can Create Requisition"),
            ("custom_update_requisition", "Can Update Requisition"),
            ("custom_delete_requisition", "Can Delete Requisition"),
            ("custom_view_requisition", "Can View Requisition"),
            ("custom_approve_requisition", "Can Approve Requisition"),
            ("custom_approve_capital_requisition", "Administration Can Approve Capital Requisition"),
            ("custom_approve_consumable_requisition", "Administration Can Approve Consumable Requisition"),
            ("custom_issue_requisition", "Stores Issue Requisition")
            
        ]

    def save(self, *args, **kwargs):
       
        if not self.id:
            number = incrementor()
            self.id = number()
            while Requisition.objects.filter(id=self.id).exists():
                self.id = number()
        super(Requisition, self).save( *args, **kwargs)


class Requisition_Details(models.Model):
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled','Cancelled'),
        ('Authorized','Authorized'),
        ('Admin Cancelled','Admin Cancelled'),
        ('Issued','Issued'),
    )
    detail_date = models.DateField(auto_now_add=True,null=True, blank=True)
    product_id = models.ForeignKey(Products, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    quantity_approved = models.IntegerField(default=0)
    quantity_issued = models.IntegerField(default=0)
    remender = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=stat, default="Pending", null=True, blank=True)
    release = models.BooleanField(default=False)
    approval = models.CharField(max_length=30, choices=stat, default='Pending', null=True, blank=True)
  
    requisition_id = models.ForeignKey(Requisition, on_delete=models.CASCADE)

    history = HistoricalRecords()
    def __str__(self):
        return self.product_id.name

    class Meta:
            
        db_table = 'Requisition_Detail'
        verbose_name = 'Requisition_Detail'
        verbose_name_plural = 'Requisition_Details'
    
    def save(self, *args, **kwargs):
        self.remender = self.quantity_approved - self.quantity_issued
        if self.quantity_approved > 0:
            self.approval = 'Authorized'
        if self.quantity_issued > 0:
            self.approval = 'Issued'
        super(Requisition_Details, self).save( *args, **kwargs)

class Allocation(models.Model):
   
    id = models.CharField(max_length=2000, primary_key=True)
    allocation_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255)
    devision  = models.ForeignKey(Devision, blank=True, null=True, related_name = 'alcdevisions',on_delete=models.CASCADE)
    release = models.BooleanField(default=False)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'allocationtenant',on_delete=models.CASCADE)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
           
        if not self.id:
            number = incrementor()
            self.id = number()
            while Allocation.objects.filter(id=self.id).exists():
                self.id = number()
        super(Allocation, self).save( *args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        
        db_table = 'Allocation'
        verbose_name = 'Allocation'
        verbose_name_plural = 'Allocations'

        permissions = [
            ("custom_create_allocation", "Can Create Allocation"),
            ("custom_update_allocation", "Can Update Allocation"),
            ("custom_delete_allocation", "Can Delete Allocation"),
            ("custom_view_allocation", "Can View Allocation"),    
        ]

class Allocation_Destination(models.Model):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
         
    )
    
    devision  = models.ForeignKey(Devision, blank=True, null=True, related_name = 'allocdevisions',on_delete=models.CASCADE)
    sub_division  = models.ForeignKey(Sub_Devision, blank=True, null=True, related_name = 'allocsub_districts',on_delete=models.CASCADE)
    classification = models.CharField(max_length=60, choices=sts, default='Consumables', null=True, blank=True)
    release = models.BooleanField(default=True)
    finish = models.BooleanField(default=False)
    allocation_id = models.ForeignKey(Allocation, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.id

    class Meta:
        
        db_table = 'Allocation_Destination'
        verbose_name = 'Allocation_Destination'
        verbose_name_plural = 'Allocation_Destinations'

       
class Allocation_Details(models.Model):
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled','Cancelled'),
        ('Authorized','Authorized'),
        ('Admin Cancelled','Admin Cancelled'),
        ('Issued','Issued'),
    )
    detail_date = models.DateField(auto_now_add=True,null=True, blank=True)
    product_id = models.ForeignKey(Products, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    quantity_issued = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=stat, default="Pending", null=True, blank=True)
    release = models.BooleanField(default=False)
    approval = models.CharField(max_length=30, choices=stat, default='Pending', null=True, blank=True)
    destination_id = models.ForeignKey(Allocation_Destination, on_delete=models.CASCADE)
    history = HistoricalRecords()
    def __str__(self):
        return self.product_id.name

    class Meta:
            
        db_table = 'Allocation_Detail'
        verbose_name = 'Allocation_Detail'
        verbose_name_plural = 'Allocation_Details'
    
    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.approval = 'Authorized'
        if self.quantity_issued > 0:
            self.approval = 'Issued'
        super(Allocation_Details, self).save( *args, **kwargs)


class Assigned_Assets (models.Model): 
    assets_id =models.ForeignKey(Assets, on_delete=models.CASCADE,null=True) 
    product_id =models.ForeignKey(Products, on_delete=models.CASCADE,null=True)
    requisition_id = models.ForeignKey(Requisition, on_delete=models.CASCADE,null=True,blank=True)
    allocation_id = models.ForeignKey(Allocation_Destination, on_delete=models.CASCADE,null=True,blank=True)
    pool = models.BooleanField(default=False)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'asset',on_delete=models.CASCADE)
    def __str__(self):
        return self.product_id.name
    
    class Meta:
        
        db_table = 'User_Assigned'
        verbose_name = 'User_Assigned'
        verbose_name_plural = 'User_Assigneds'

class Closing_Stock(models.Model):
    closing_date = models.DateTimeField(null=True, blank=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'close',on_delete=models.CASCADE)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.id:
            self.closing_date = timezone.now()
        super(Closing_Stock,self).save(*args, **kwargs)  

    def __str__(self):
        return self.id

    class Meta:
        
        db_table = 'Closing-Stock'
        verbose_name = 'Closing-Stock'
        verbose_name_plural = 'Closing-Stocks'


class Closing_Stock_Inventory(models.Model):
    closing_id =models.ForeignKey(Closing_Stock,related_name ='closing', on_delete=models.CASCADE,null=True, blank=True)
    product_id =models.ForeignKey(Products,related_name ='closingstock' ,on_delete=models.CASCADE,null=True, blank=True)
    avialable_quantity = models.PositiveIntegerField(default=0)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'tenant_closing_stock',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        
        db_table = 'Closing-Stock-Inventory'
        verbose_name = 'Closing-Stock-Inventory'
        verbose_name_plural = 'Closing-Stock-Inventorys'



class Closing_Stock_Inventory_Details(models.Model):
    closing_inventory_id =models.ForeignKey(Closing_Stock_Inventory,related_name ='closing_inventory_details', on_delete=models.CASCADE,null=True, blank=True)
    quantity_intake = models.PositiveIntegerField(default=0)
    quantity_requested = models.PositiveIntegerField(default=0)
    avialable_quantity = models.PositiveIntegerField(default=0)
    batch_number =  models.CharField(max_length=250)
    date_received = models.DateField(auto_now_add=True)
    expiring_date  = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['expiring_date']

    def __str__(self):
        return str(self.id)
    
    class Meta:
        
        db_table = 'Closing-Stock-Inventory-Detail'
        verbose_name = 'Closing-Stock-Inventory-Detail'
        verbose_name_plural = 'Closing-Stock-Inventory-Details'

   
       