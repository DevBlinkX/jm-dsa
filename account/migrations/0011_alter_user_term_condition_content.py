# Generated by Django 4.0 on 2022-10-06 11:03

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_user_total_kyc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='term_condition_content',
            field=tinymce.models.HTMLField(blank=True, max_length=2500, null=True),
        ),
    ]