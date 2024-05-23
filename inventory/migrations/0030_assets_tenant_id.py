# Generated by Django 4.1.10 on 2023-07-26 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        ('inventory', '0029_remove_products_brand_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='assets',
            name='tenant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='company.tenants'),
        ),
    ]