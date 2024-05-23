from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
# from authentication.models import User
import authentication

class Tenants(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255,null=True)
    status = models.BooleanField(default=False)
    class Meta:
        db_table = 'Tenant'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'


    def __str__(self):
        return f"{self.code } { self.name}"


class Devision(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255,null=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'devisions',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
   
    class Meta:
        db_table = 'Devision'
        verbose_name = 'Devision'
        verbose_name_plural = 'Devisions'

        permissions = [
            ("custom_create_devision", "Can Create Devison"),
            ("custom_delete_devision", "Can Delete Devison"),
            ("custom_update_devision", "Can Update Devison"),
            ("custom_view_devision", "Can View Devison"),
            ("custom_approve_devision", "Can Approve Devison"),
        ]

    def __str__(self):
        return f"{self.code } { self.name} ---- {self.tenant_id}"

class Sub_Devision(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255,null=True)
    location = models.ForeignKey('fixedassets.Location', related_name='subdevisionlocation', 
        on_delete=models.CASCADE,null=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'tenant_devisions',on_delete=models.CASCADE)
    devision  = models.ForeignKey(
        Devision, blank=True, null=True, related_name = 'sub_devisions',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    tag = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Sub_Devision'
        verbose_name = 'Sub_Devision'
        verbose_name_plural = 'Sub_Devisions'

        permissions = [
            ("custom_create_sub_devision", "Can Create Sub_Devision"),
            ("custom_delete_sub_devision", "Can Delete Sub_Devision"),
            ("custom_update_sub_devision", "Can Update Sub_Devision"),
            ("custom_view_sub_devision", "Can View Sub_Devision"),
        ]
    def __str__(self):
        return self.name

class Approvals(models.Model):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
        ('All','All'),
         
    )
    st= (
        ('First','First'),
        ('Second','Second'),
        ('Third','Third'),
         
    )
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'tenant_approval',on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        'authentication.User', blank=True, null=True, related_name = 'user_approval',on_delete=models.CASCADE)
    classification = models.CharField(max_length=50, choices=sts, null=True, blank=True)
    type_of_approval = models.CharField(max_length=50, choices=st, null=True, blank=True)
    
    class Meta:
        db_table = 'Approval'
        verbose_name = 'Approval'
        verbose_name_plural = 'Approvals'

       
    def __str__(self):
        return self.user_id