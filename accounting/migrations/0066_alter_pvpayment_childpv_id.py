# Generated by Django 4.1.6 on 2024-05-17 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0065_pvpayment_childpv_id_alter_pvpayment_pv_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pvpayment',
            name='childpv_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pvchild', to='accounting.paymentvoucher'),
        ),
    ]