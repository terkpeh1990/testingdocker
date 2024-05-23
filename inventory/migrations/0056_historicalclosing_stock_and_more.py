# Generated by Django 4.1.10 on 2023-08-07 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_approvals'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0055_allocation_destination_finish_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalClosing_Stock',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('closing_date', models.DateField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tenant_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.tenants')),
            ],
            options={
                'verbose_name': 'historical Closing-Stock',
                'verbose_name_plural': 'historical Closing-Stocks',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Closing_Stock_Inventory_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_intake', models.PositiveIntegerField(default=0)),
                ('quantity_requested', models.PositiveIntegerField(default=0)),
                ('avialable_quantity', models.PositiveIntegerField(default=0)),
                ('batch_number', models.CharField(max_length=250)),
                ('date_received', models.DateField(auto_now_add=True)),
                ('expiring_date', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('closing_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='closing_inventory_details', to='inventory.inventory')),
            ],
            options={
                'ordering': ['expiring_date'],
            },
        ),
        migrations.CreateModel(
            name='Closing_Stock_Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avialable_quantity', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='closingstock', to='inventory.products')),
                ('tenant_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_closing_stock', to='company.tenants')),
            ],
        ),
        migrations.CreateModel(
            name='Closing_Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('closing_date', models.DateField(blank=True, null=True)),
                ('tenant_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='close', to='company.tenants')),
            ],
            options={
                'verbose_name': 'Closing-Stock',
                'verbose_name_plural': 'Closing-Stocks',
                'db_table': 'Closing-Stock',
            },
        ),
    ]
