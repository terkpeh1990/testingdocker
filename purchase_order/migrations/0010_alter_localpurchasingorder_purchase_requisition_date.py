# Generated by Django 4.1.6 on 2024-02-01 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0009_purchaserequisition_release'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localpurchasingorder',
            name='purchase_requisition_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
