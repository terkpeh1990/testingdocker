# Generated by Django 4.1.6 on 2024-04-15 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0015_agentticket_completed_days_agentticket_elapsed_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentticket',
            name='expected_days',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
