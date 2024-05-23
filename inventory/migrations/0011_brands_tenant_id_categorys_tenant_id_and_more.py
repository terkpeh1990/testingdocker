# Generated by Django 4.1.10 on 2023-07-24 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        ('inventory', '0010_alter_products_type_of_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='brands',
            name='tenant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand', to='company.tenants'),
        ),
        migrations.AddField(
            model_name='categorys',
            name='tenant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='company.tenants'),
        ),
        migrations.AddField(
            model_name='products',
            name='tenant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='company.tenants'),
        ),
        migrations.AddField(
            model_name='unit_of_measurement',
            name='tenant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unit', to='company.tenants'),
        ),
    ]