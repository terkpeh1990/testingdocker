from django.db import models
from company.models import *

# Create your models here.
class appmodules(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'Systemconfig'
        verbose_name = 'Systemconfig'
        verbose_name_plural = 'Systemconfigs'    

        permissions = [
            ("custom_access_to_inventory", "Have Access To Inventory"),
            ("custom_access_to_accounting", "Have Access To Accounting"),
            ("custom_access_to_dms", "Have Access To DMS"),
            ("custom_access_to_helpdesk", "Have Access To Helpdesk"),
            ("custom_access_to_fixedasset", "Have Access To Fixed Asset"),
            ("custom_access_to_pensions", "Have Access To Pensions"),
            
        ]

    def __str__(self):
        return self.name

class Companymodule(models.Model):
    tenant_id = models.ForeignKey(
        Tenants, blank=True, null=True, related_name = 'companyapp',on_delete=models.CASCADE)
    app = models.ForeignKey(
        appmodules, blank=True, null=True, related_name = 'app',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.app.name} ---- {self.tenant_id.name}"

