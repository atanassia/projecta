# Generated by Django 4.1.2 on 2022-10-26 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0013_remove_checkstatus__check_checkstatus_check_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkstatus',
            old_name='check_id',
            new_name='_check',
        ),
    ]
