# Generated by Django 4.1.4 on 2023-02-08 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0062_agreementstatus_is_delete_clientstatus_is_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='reasons_termination',
            field=models.TextField(blank=True, null=True, verbose_name='Причины расторжения договора'),
        ),
    ]
