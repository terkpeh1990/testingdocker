# Generated by Django 4.1.6 on 2024-04-10 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0071_remove_job_detail_brand_id_remove_job_detail_funding_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_certification',
            name='driver_contact',
        ),
        migrations.RemoveField(
            model_name='job_certification',
            name='driver_name',
        ),
    ]
