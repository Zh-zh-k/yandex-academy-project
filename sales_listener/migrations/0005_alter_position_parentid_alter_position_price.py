# Generated by Django 4.0.5 on 2022-06-26 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_listener', '0004_alter_position_parentid_alter_position_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='parentId',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='price',
            field=models.BigIntegerField(null=True),
        ),
    ]
