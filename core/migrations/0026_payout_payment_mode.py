# Generated by Django 4.0 on 2023-03-22 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_payout_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payout',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('IMPS', 'IMPS'), ('NEFT', 'NEFT')], max_length=100, null=True),
        ),
    ]
