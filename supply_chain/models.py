from django.db import models
from company.models import *
from authentication.models import *
from django.conf import settings
from inventory.utils import *
from dms.validators import validate_file_extension
from decimal import Decimal
# Create your models here.


class Annual_Budget(models.Model):
    sts= (
        ('Active','Active'),
        ('In Active','In Active'),
         
    )
    period = models.CharField(max_length=250,blank=True, null=True)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    amount_left = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    status = models.CharField(max_length=50, choices= sts,blank=True, null=True)
    

    class Meta:
        
        db_table = 'Annual_Budget'
        verbose_name = 'Annual_Budget'
        verbose_name_plural = 'Annual_Budgets'

        permissions = [
            ("custom_create_budget", "Can Create Budget"),
            ("custom_approve_budget", "Can Approve Budget"),
            ("custom_cancel_budget", "Can Cancel Budget"),
            ("custom_view_budget", "Can View Budget"),
        ]

    def __str__(self):
        return f"{self.period} --- {self.amount_left}"

    def save(self, *args, **kwargs):
        self.amount_left = Decimal(self.budget_amount) - Decimal(self.amount_spent)
        super(Annual_Budget, self).save( *args, **kwargs)


class Supply_Chain_Requisition(models.Model):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
         
    )
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled','Cancelled'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    requisition_date = models.DateField(null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=stat, default="Pending", null=True, blank=True)
    release = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.id

    class Meta:
        
        db_table = 'Supply_Chain_Requisition'
        verbose_name = 'Supply_Chain_Requisition'
        verbose_name_plural = 'Supply_Chain_Requisitions'

        permissions = [
            ("custom_create_requisition", "Can Create Requisition"),
            ("custom_update_requisition", "Can Update Requisition"),
            ("custom_delete_requisition", "Can Delete Requisition"),
            ("custom_view_requisition", "Can View Requisition"),
            ("custom_approve_requisition", "Can Approve Requisition"),
            ("custom_cancel_requisition", "Can Cancel Requisition"),
            
            
        ]

    def save(self, *args, **kwargs):
       
        if not self.id:
            number = incrementor()
            self.id = number()
            while Supply_Chain_Requisition.objects.filter(id=self.id).exists():
                self.id = number()
        super(Supply_Chain_Requisition, self).save( *args, **kwargs)


class Supply_Chain_Requisition_Details(models.Model):
    detail_date = models.DateField(auto_now_add=True,null=True, blank=True)
    product = models.CharField(max_length=255,blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    requisition_id = models.ForeignKey(Supply_Chain_Requisition, on_delete=models.CASCADE)
    history = HistoricalRecords()
    def __str__(self):
        return self.product.name

    class Meta:
            
        db_table = 'Supply_Chain_Requisition_Details'
        verbose_name = 'Supply_Chain_Requisition_Details'
        verbose_name_plural = 'Supply_Chain_Requisition_Details'
    def save(self, *args, **kwargs):
        self.total_price = Decimal(self.unit_price) - Decimal(self.quantity)
        super(Supply_Chain_Requisition_Details, self).save( *args, **kwargs)