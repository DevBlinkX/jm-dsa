# Generated by Django 4.0 on 2022-11-01 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_tdscertificate_tds_certificate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tdscertificate',
            name='quarter_month',
        ),
        migrations.AddField(
            model_name='tdscertificate',
            name='quarter',
            field=models.CharField(choices=[('1', 'First Quarter'), ('2', 'Second Quarter'), ('3', 'Third Quarter'), ('4', 'Fourth Quarter')], max_length=100, null=True),
        ),
    ]