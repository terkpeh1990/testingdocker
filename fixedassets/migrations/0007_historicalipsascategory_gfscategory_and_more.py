# Generated by Django 4.1.6 on 2024-03-07 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fixedassets', '0006_remove_historicalipsascategory_gfscategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalipsascategory',
            name='gfscategory',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fixedassets.gfscategory'),
        ),
        migrations.AddField(
            model_name='ipsascategory',
            name='gfscategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ipsasgfscategory', to='fixedassets.gfscategory'),
        ),
    ]
