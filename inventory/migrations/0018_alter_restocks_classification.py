# Generated by Django 4.1.10 on 2023-07-25 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_alter_restock_details_batch_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restocks',
            name='classification',
            field=models.CharField(blank=True, choices=[('Capital', 'Capital'), ('Consumables', 'Consumables')], default='Consumables', max_length=50, null=True),
        ),
    ]