# Generated by Django 4.0 on 2022-10-31 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_timingslot'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='term_condition_agree_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]