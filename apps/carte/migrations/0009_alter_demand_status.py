# Generated by Django 4.0.2 on 2022-02-19 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0008_demand_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('accepted', 'Accepted'), ('refused', 'Refused')], default='active', max_length=255),
        ),
    ]