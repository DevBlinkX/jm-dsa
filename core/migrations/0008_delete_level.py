# Generated by Django 4.0 on 2022-10-04 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_incentive_leads_rename_date_payout_voucher_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Level',
        ),
    ]
