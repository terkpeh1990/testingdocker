from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from simple_history.models import HistoricalRecords
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group
from company.models import *




class Grade(models.Model):
    name = models.CharField(max_length=100)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'grades',on_delete=models.CASCADE)
    history = HistoricalRecords()
    class Meta:
        db_table = 'Rank'
        verbose_name = 'Rank'
        verbose_name_plural = 'Ranks'

        permissions = [
            ("custom_create_rank", "Can Create Rank"),
            ("custom_delete_rank", "Can Delete Rank"),
            ("custom_update_rank", "Can Update Rank"),
            ("custom_view_Rank", "Can View Rank"),
        ]

    def __str__(self):
        return self.name
    


class User(AbstractUser):
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 

     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    staffid = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20,validators=[phone_regex],null=True)
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'users',on_delete=models.CASCADE)
    devision  = models.ForeignKey(Devision, blank=True, null=True, related_name = 'devisions',on_delete=models.CASCADE)
    sub_division  = models.ForeignKey(Sub_Devision, blank=True, null=True, related_name = 'sub_districts',on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, blank=True, null=True, related_name = 'grades',on_delete=models.CASCADE)
    group  = models.ForeignKey(Group, blank=True, null=True, related_name = 'groups',on_delete=models.CASCADE)
    email = models.CharField(max_length=200,unique=True)
    hq = models.BooleanField(default=False)
    password = models.CharField(max_length=255, blank=True, null=True)  
    is_admin = models.BooleanField(default=False)
    is_new =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    # history = HistoricalRecords()

    class Meta:
        
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        permissions = [
            ("custom_create_user", "Can Create User"),
            ("custom_delete_user", "Can Delete User"),
            ("custom_update_user", "Can Update User"),
            ("custom_view_user", "Can View User"),
            ("custom_view_report", "Can View Reports"),
        ]
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.last_name } {self.first_name }"