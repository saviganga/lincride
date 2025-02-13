# Generated by Django 3.2.9 on 2025-02-13 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='pricingconfiguration',
            index=models.Index(fields=['demand_level', 'traffic_level'], name='pricing_pri_demand__f033ea_idx'),
        ),
    ]
