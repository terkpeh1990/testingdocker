# Generated by Django 4.1.10 on 2023-10-05 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0028_alter_paymentvoucher_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentvoucher',
            name='authorized_and_passed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authorizedpassedby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentvoucher',
            name='authorized_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authorizedby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentvoucher',
            name='paid_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paidby', to=settings.AUTH_USER_MODEL),
        ),
    ]