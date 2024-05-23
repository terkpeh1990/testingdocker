# Generated by Django 4.1.10 on 2023-10-04 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dms', '0037_alter_document_options_document_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_from',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='document_from_grade',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='document_through',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='document_through_grade',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='document_to',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='document_to_grade',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]