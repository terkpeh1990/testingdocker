# Generated by Django 4.1.10 on 2023-07-19 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_brands_options_alter_categorys_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avialable_quantity', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.brands')),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.categorys')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='inventory.products')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_intake', models.PositiveIntegerField(default=0)),
                ('quantity_requested', models.PositiveIntegerField(default=0)),
                ('avialable_quantity', models.PositiveIntegerField(default=0)),
                ('batch_number', models.CharField(max_length=250)),
                ('date_received', models.DateField(auto_now_add=True)),
                ('expiring_date', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.brands')),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.categorys')),
                ('inventory_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory_details', to='inventory.inventory')),
            ],
            options={
                'ordering': ['expiring_date'],
            },
        ),
    ]
