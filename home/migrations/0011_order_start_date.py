# Generated by Django 4.2.1 on 2023-06-03 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_order_smart_contract_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='start_date',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
    ]
