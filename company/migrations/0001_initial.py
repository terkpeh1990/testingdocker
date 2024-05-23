# Generated by Django 4.1.10 on 2023-07-23 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Devision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Devision',
                'verbose_name_plural': 'Devisions',
                'db_table': 'Devision',
                'permissions': [('custom_create_devision', 'Can Create Devison'), ('custom_delete_devision', 'Can Delete Devison'), ('custom_update_devision', 'Can Update Devison'), ('custom_view_devision', 'Can View Devison'), ('custom_approve_devision', 'Can Approve Devison')],
            },
        ),
        migrations.CreateModel(
            name='Tenants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Tenant',
                'verbose_name_plural': 'Tenants',
                'db_table': 'Tenant',
            },
        ),
        migrations.CreateModel(
            name='Sub_Devision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('devision', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_devisions', to='company.devision')),
                ('tenant_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_devisions', to='company.tenants')),
            ],
            options={
                'verbose_name': 'Sub_Devision',
                'verbose_name_plural': 'Sub_Devisions',
                'db_table': 'Sub_Devision',
                'permissions': [('custom_create_sub_devision', 'Can Create Sub_Devision'), ('custom_delete_sub_devision', 'Can Delete Sub_Devision'), ('custom_update_sub_devision', 'Can Update Sub_Devision'), ('custom_view_sub_devision', 'Can View Sub_Devision')],
            },
        ),
        migrations.AddField(
            model_name='devision',
            name='tenant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devisions', to='company.tenants'),
        ),
    ]
