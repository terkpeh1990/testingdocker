# Generated by Django 4.1.6 on 2024-03-25 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0059_alter_imprest_amount'),
        ('fixedassets', '0037_alter_reevaluation_accountingyear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reevaluation',
            name='accountingyear',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluateaccountingyear', to='accounting.fiscal_year'),
        ),
    ]