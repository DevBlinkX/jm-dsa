# Generated by Django 4.0 on 2023-01-16 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_address_options_alter_bankdetail_options_and_more'),
        ('core', '0020_alter_brokerage_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incentive',
            name='dra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incentives', to='account.user'),
        ),
    ]
