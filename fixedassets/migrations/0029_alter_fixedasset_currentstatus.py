# Generated by Django 4.1.6 on 2024-03-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixedassets', '0028_fixedasset_status_alter_fixedasset_currentstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedasset',
            name='currentstatus',
            field=models.CharField(choices=[('In Use', 'In Use'), ('Not in Use', 'Not in Use'), ('Retired', 'Retired'), ('Disposed', 'Disposed'), ('On-going', 'On-going'), ('Abandoned', 'Abandoned'), ('Suspended', 'Suspended')], default='In Use', max_length=30, null=True),
        ),
    ]
