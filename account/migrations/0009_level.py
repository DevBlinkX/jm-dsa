# Generated by Django 4.0 on 2022-10-04 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_user_admin_status_user_mx_referred_dra_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='leaderboard/level/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
