# Generated by Django 4.1.10 on 2023-10-16 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0045_alter_paymentvoucherbeneficiary_amount_received'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentvoucherbeneficiary',
            name='status',
            field=models.CharField(choices=[('Awaiting Payment', 'Awaiting Payment'), ('Recipient Notified', 'Recipient Notified'), ('Amount Paid', 'Amount Paid')], default='Awaiting Payment', max_length=60),
        ),
    ]