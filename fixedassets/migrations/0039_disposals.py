# Generated by Django 4.1.6 on 2024-03-25 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0059_alter_imprest_amount'),
        ('fixedassets', '0038_alter_reevaluation_accountingyear'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disposals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desposal_date', models.DateField(null=True)),
                ('methodofdesposal', models.CharField(choices=[('Sales', 'Sales'), ('Auction', 'Auction'), ('Donated', 'Donated'), ('Trade-in/Exchanged', 'Trade-in/Exchanged'), ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'), ('Scrapped', 'Scrapped')], max_length=50, null=True)),
                ('proceedsfromsales', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('accountingyear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disposalaccountingyear', to='accounting.fiscal_year')),
                ('asset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disposalasset', to='fixedassets.fixedasset')),
            ],
            options={
                'verbose_name': 'Disposal',
                'verbose_name_plural': 'Disposals',
                'db_table': 'Disposals',
            },
        ),
    ]
