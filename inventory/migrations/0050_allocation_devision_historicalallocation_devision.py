# Generated by Django 4.1.10 on 2023-08-02 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_approvals'),
        ('inventory', '0049_allocation_allocation_destination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocation',
            name='devision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alcdevisions', to='company.devision'),
        ),
        migrations.AddField(
            model_name='historicalallocation',
            name='devision',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.devision'),
        ),
    ]
