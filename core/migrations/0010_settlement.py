# Generated by Django 4.0 on 2022-10-07 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_user_dra_code_encrypted'),
        ('core', '0009_knowlagecenter_is_trending'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('month', models.CharField(max_length=100, null=True)),
                ('year', models.CharField(max_length=100, null=True)),
                ('converted', models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True)),
                ('trad_active', models.BooleanField(default=True)),
                ('gross_brokerage', models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True)),
                ('incentive', models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True)),
                ('net_brokerage', models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True)),
                ('dra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]