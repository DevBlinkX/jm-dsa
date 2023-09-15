# Generated by Django 4.0 on 2023-03-22 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_rename_term_condition_content_user_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('dra', 'DRA'), ('rm', 'RM'), ('dsa', 'DSA'), ('rmj', 'RMJ')], default='dra', max_length=100, null=True),
        ),
    ]