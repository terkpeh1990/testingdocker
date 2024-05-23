# Generated by Django 4.1.10 on 2023-09-07 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dms', '0014_remove_document_classification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'permissions': [('custom_create_document', 'Can Create Document'), ('custom_delete_document', 'Can Delete Document'), ('custom_delete_change_status', 'Can Change Status of Document'), ('custom_create_document_for', 'custom_create_document_for')], 'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
    ]