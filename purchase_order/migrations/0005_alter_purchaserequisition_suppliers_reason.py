# Generated by Django 4.1.6 on 2024-02-01 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0004_alter_purchaserequisition_suppliers_supplier_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaserequisition_suppliers',
            name='reason',
            field=models.CharField(blank=True, max_length=1200, null=True),
        ),
    ]
