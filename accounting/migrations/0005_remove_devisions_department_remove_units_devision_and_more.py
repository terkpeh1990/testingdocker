# Generated by Django 4.1.10 on 2023-08-22 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_rename_unit_units_devision'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devisions',
            name='department',
        ),
        migrations.RemoveField(
            model_name='units',
            name='devision',
        ),
        migrations.DeleteModel(
            name='Departments',
        ),
        migrations.DeleteModel(
            name='Devisions',
        ),
        migrations.DeleteModel(
            name='Units',
        ),
    ]