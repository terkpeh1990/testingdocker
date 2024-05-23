# Generated by Django 4.1.6 on 2023-12-20 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supply_chain', '0002_alter_annual_budget_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supply_Chain_Requisition',
            fields=[
                ('id', models.CharField(max_length=2000, primary_key=True, serialize=False)),
                ('requisition_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20, null=True)),
                ('release', models.BooleanField(default=False)),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Supply_Chain_Requisition',
                'verbose_name_plural': 'Supply_Chain_Requisitions',
                'db_table': 'Supply_Chain_Requisition',
                'permissions': [('custom_create_requisition', 'Can Create Requisition'), ('custom_update_requisition', 'Can Update Requisition'), ('custom_delete_requisition', 'Can Delete Requisition'), ('custom_view_requisition', 'Can View Requisition'), ('custom_approve_requisition', 'Can Approve Requisition'), ('custom_cancel_requisition', 'Can Cancel Requisition')],
            },
        ),
        migrations.CreateModel(
            name='Supply_Chain_Requisition_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_date', models.DateField(auto_now_add=True, null=True)),
                ('product', models.CharField(blank=True, max_length=255, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('requisition_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supply_chain.supply_chain_requisition')),
            ],
            options={
                'verbose_name': 'Supply_Chain_Requisition_Details',
                'verbose_name_plural': 'Supply_Chain_Requisition_Details',
                'db_table': 'Supply_Chain_Requisition_Details',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSupply_Chain_Requisition_Details',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('detail_date', models.DateField(blank=True, editable=False, null=True)),
                ('product', models.CharField(blank=True, max_length=255, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('requisition_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='supply_chain.supply_chain_requisition')),
            ],
            options={
                'verbose_name': 'historical Supply_Chain_Requisition_Details',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSupply_Chain_Requisition',
            fields=[
                ('id', models.CharField(db_index=True, max_length=2000)),
                ('requisition_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20, null=True)),
                ('release', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Supply_Chain_Requisition',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]