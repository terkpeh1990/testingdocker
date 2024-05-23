# Generated by Django 4.1.6 on 2024-04-09 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0007_alter_agent_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agentlevel', to='helpdesk.level'),
        ),
    ]
