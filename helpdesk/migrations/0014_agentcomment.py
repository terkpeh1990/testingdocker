# Generated by Django 4.1.6 on 2024-04-15 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0013_agentticket_level_alter_agentticket_agent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1200)),
                ('commentdate', models.DateField(blank=True, null=True)),
                ('commenttime', models.TimeField(blank=True, null=True)),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solution', to='helpdesk.agent')),
                ('ticket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agentcomment', to='helpdesk.ticket')),
            ],
            options={
                'verbose_name': 'AgentComment',
                'verbose_name_plural': 'AgentComments',
                'db_table': '',
                'managed': True,
            },
        ),
    ]