from django.db import models
from authentication.models import User
from inventory.models import Products,Supplier
from inventory.utils import *

# Create your models here.
class PurchaseRequisition(models.Model):
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled','Cancelled'),
        ('LPO Created','LPO Created'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    purchase_requisition_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=stat, default="Pending", null=True, blank=True)
    product_id = models.ForeignKey(Products,related_name='purchaserequisition_products', on_delete= models.CASCADE,null=True, blank=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    total_amount =  models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    supplier_id = models.ForeignKey(Supplier,related_name='active_supplier',null=True, blank=True, on_delete= models.CASCADE)
    release = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    class Meta:
        
        db_table = 'PurchaseRequisition'
        verbose_name = 'PurchaseRequisition'
        verbose_name_plural = 'PurchaseRequisitions'

        permissions = [
            ("custom_create_purchase_requisition", "Can Create PurchaseRequisition"),
            ("custom_update_purchase_requisition", "Can Update PurchaseRequisition"),
            ("custom_delete_purchase_requisition", "Can Delete PurchaseRequisition"),
            ("custom_view_purchase_requisition", "Can View PurchaseRequisition"),
            ("custom_approve_purchase_requisition", "Can Approve PurchaseRequisition"),
            
        ]

    def save(self, *args, **kwargs):
        self.total_amount = self.unit_price*self.quantity
        if not self.id:
            number = incrementor()
            self.id = number()
            while PurchaseRequisition.objects.filter(id=self.id).exists():
                self.id = number()
        super(PurchaseRequisition, self).save( *args, **kwargs)

class PurchaseRequisition_Suppliers(models.Model):
    stat = (
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    )
    supplier_id = models.ForeignKey(Supplier,related_name='purchase_suppliers', on_delete= models.CASCADE)
    amount =  models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    purchase_requisition_id = models.ForeignKey(PurchaseRequisition,related_name='purchaseitems', on_delete=models.CASCADE,null=True, blank=True)
    reason  = models.CharField(max_length=1200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=stat, null=True, blank=True)

    def __str__(self):
        return self.product.name

    class Meta:
            
        db_table = 'PurchaseRequisition_Supplier'
        verbose_name = 'PurchaseRequisition_Supplier'
        verbose_name_plural = 'PurchaseRequisition_Supplier'


class LocalPurchasingOrder(models.Model):
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled','Cancelled'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    lpo_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=stat, default="Pending", null=True, blank=True)
    product_id = models.ForeignKey(Products,related_name='lpon_products', on_delete= models.CASCADE,null=True, blank=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    total_amount =  models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True, blank=True)
    supplier_id = models.ForeignKey(Supplier,related_name='lpo_supplier',null=True, blank=True, on_delete= models.CASCADE)
    purchase_requisition_id = models.ForeignKey(PurchaseRequisition,related_name='lpopurchaserequisition', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        
        db_table = 'LocalPurchasingOrdern'
        verbose_name = 'LocalPurchasingOrder'
        verbose_name_plural = 'LocalPurchasingOrders'

        permissions = [
            ("custom_create_lpo", "Can Create LPO"),
            ("custom_update_lpo", "Can Update LPO"),
            ("custom_delete_lpo", "Can Delete LPO"),
            ("custom_view_lpo", "Can View LPO"),
            ("custom_approve_lpo", "Can Approve LPO"),
            
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = number()
            while LocalPurchasingOrder.objects.filter(id=self.id).exists():
                self.id = number()
        super(LocalPurchasingOrder, self).save( *args, **kwargs)
    
   
