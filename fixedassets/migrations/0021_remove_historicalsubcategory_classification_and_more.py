# Generated by Django 4.1.6 on 2024-03-13 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fixedassets', '0020_fixedasset_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsubcategory',
            name='classification',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='classification',
        ),
    ]
