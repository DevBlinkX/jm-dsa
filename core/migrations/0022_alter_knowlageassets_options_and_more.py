# Generated by Django 4.0 on 2023-01-30 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_incentive_dra'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='knowlageassets',
            options={'verbose_name': 'Brand Assets', 'verbose_name_plural': 'Brand Assets'},
        ),
        migrations.AlterField(
            model_name='knowlagecenter',
            name='image',
            field=models.ImageField(blank=True, help_text='Image should be in 1920*1080px dimension', null=True, upload_to='knowlage-center-image/'),
        ),
    ]