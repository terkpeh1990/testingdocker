# Generated by Django 4.1.6 on 2024-03-10 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixedassets', '0015_rename_condition_fixedasset_conditions'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixedasset',
            name='registrationnumber',
            field=models.CharField(error_messages={'unique': 'Vehicle With this Registration number already exist.'}, max_length=255, null=True, unique=True),
        ),
    ]
