# Generated by Django 4.0.2 on 2022-02-12 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0004_alter_carte_code_alter_transfer_from_carte_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.AddField(
            model_name='transaction',
            name='carte',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='historic', to='carte.carte'),
            preserve_default=False,
        ),
    ]
