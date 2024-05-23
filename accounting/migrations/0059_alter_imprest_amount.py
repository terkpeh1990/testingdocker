# Generated by Django 4.1.10 on 2023-11-17 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0058_alter_imprest_actual_expense_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imprest',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
