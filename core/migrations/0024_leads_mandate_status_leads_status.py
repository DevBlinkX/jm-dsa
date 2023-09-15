# Generated by Django 4.0 on 2023-03-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_remove_tdscertificate_segment'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='mandate_status',
            field=models.CharField(blank=True, choices=[('Not Initiated', 'Not Initiated'), ('In-Process', 'In-Process'), ('Rejected', 'Rejected'), ('Disbursed', 'Disbursed')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='leads',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]