# Generated by Django 4.1.10 on 2023-09-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dms', '0019_alter_documentbudget_paragraph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentbudget',
            name='paragraph',
            field=models.CharField(max_length=1200),
        ),
    ]
