# Generated by Django 4.0.5 on 2022-06-26 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_listener', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='uuid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='position',
            old_name='posType',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='position',
            name='children',
        ),
        migrations.RemoveField(
            model_name='position',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='position',
            name='published_date',
        ),
        migrations.RemoveField(
            model_name='position',
            name='text',
        ),
    ]
