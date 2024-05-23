# Generated by Django 4.1.6 on 2024-03-09 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0026_alter_historicalgrade_options_and_more'),
        ('inventory', '0069_remove_job_certification_lpo_id_and_more'),
        ('company', '0005_sub_devision_tag'),
        ('fixedassets', '0009_mothodofacquisition_historicalmothodofacquisition'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_id', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('amotization', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=4, null=True)),
                ('usage', models.CharField(choices=[('Public Domain', 'Public Domain'), ('Private Domain', 'Private Domain')], max_length=17, null=True)),
                ('size', models.CharField(max_length=255, null=True)),
                ('ghanapostgpsaddress', models.CharField(max_length=255, null=True)),
                ('titled', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=4, null=True)),
                ('staffid', models.CharField(max_length=255, null=True)),
                ('fullname', models.CharField(max_length=255, null=True)),
                ('currentstatus', models.CharField(choices=[('In Use', 'In Use'), ('Not in Use', 'Not in Use'), ('Retired', 'Retired'), ('Disposed', 'Disposed')], max_length=30, null=True)),
                ('investmentproperty', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=4, null=True)),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('usefullife', models.PositiveIntegerField(default=0, null=True)),
                ('desposal_date', models.DateField(null=True)),
                ('methodofdesposal', models.CharField(choices=[('Sales', 'Sales'), ('Auction', 'Auction'), ('Donated', 'Donated'), ('Trade-in/Exchanged', 'Trade-in/Exchanged'), ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'), ('Scrapped', 'Scrapped')], max_length=50, null=True)),
                ('proceedsfromsales', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('comments', models.CharField(max_length=255, null=True)),
                ('accountingrecognition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accountingrecognition', to='fixedassets.accountingrecognition')),
                ('classification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classification', to='fixedassets.classification')),
                ('costcenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assetcostcenter', to='company.devision')),
                ('fundsource', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assetfundsource', to='fixedassets.sourceoffunding')),
                ('gfscategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gfscategory', to='fixedassets.gfscategory')),
                ('ipsascategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ipsascategory', to='fixedassets.ipsascategory')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assetlocation', to='fixedassets.location')),
                ('methodofacquisition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assetmethodofacquisition', to='fixedassets.mothodofacquisition')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position', to='authentication.grade')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assetproduct', to='inventory.products')),
                ('subcostcenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assetsubcostcenter', to='company.sub_devision')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
                'db_table': 'Assets',
                'permissions': [('custom_create_assets', 'Can Create Assets'), ('custom_view_assets', 'Can View Assets'), ('custom_delete_assets', 'Can Delete Assets'), ('custom_run_depreciation', 'Can Run Depreciaition on Assets')],
            },
        ),
    ]