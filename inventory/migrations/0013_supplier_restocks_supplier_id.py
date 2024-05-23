# Generated by Django 4.1.10 on 2023-07-24 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        ('inventory', '0012_restocks_restock_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('country', models.CharField(blank=True, max_length=250, null=True)),
                ('tenant_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='company.tenants')),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
                'db_table': 'Supplier',
                'permissions': [('custom_create_supplier', 'Can Create Supplier'), ('custom_update_supplier', 'Can Update Supplier'), ('custom_delete_supplier', 'Can Delete Supplier'), ('custom_view_supplier', 'Can View Supplier')],
            },
        ),
        migrations.AddField(
            model_name='restocks',
            name='supplier_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='inventory.supplier'),
        ),
    ]
