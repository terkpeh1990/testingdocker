# Generated by Django 4.1.10 on 2023-10-04 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0024_alter_paymentvoucher_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentvoucher',
            name='withholding_tax_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]