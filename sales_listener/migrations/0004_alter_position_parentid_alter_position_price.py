# Generated by Django 4.0.5 on 2022-06-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_listener', '0003_rename_datetime_position_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='parentId',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='price',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
