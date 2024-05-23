# Generated by Django 4.1.10 on 2023-07-26 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_job_certification_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_detail',
            name='expiring_date',
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=10),
        ),
    ]
