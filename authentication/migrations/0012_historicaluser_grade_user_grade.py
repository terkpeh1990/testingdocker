# Generated by Django 4.1.10 on 2023-07-15 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_remove_historicaluser_group_remove_user_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='grade',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.grade'),
        ),
        migrations.AddField(
            model_name='user',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='authentication.grade'),
        ),
    ]
