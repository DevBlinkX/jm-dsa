# Generated by Django 4.0 on 2023-01-30 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_address_options_alter_bankdetail_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='bg_colour',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
