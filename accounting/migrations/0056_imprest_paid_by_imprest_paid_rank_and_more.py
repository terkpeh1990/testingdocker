# Generated by Django 4.1.10 on 2023-10-24 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0055_alter_imprest_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='imprest',
            name='paid_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aipaidby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='imprest',
            name='paid_rank',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
        migrations.AddField(
            model_name='imprest',
            name='paid_sub_division',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='imprest',
            name='certified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aicertifiedby', to=settings.AUTH_USER_MODEL),
        ),
    ]