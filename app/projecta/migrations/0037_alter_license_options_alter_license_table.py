# Generated by Django 4.1.2 on 2022-11-24 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0036_alter_agreement_licence'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='license',
            options={'verbose_name': 'Лицензия', 'verbose_name_plural': 'Лицензии'},
        ),
        migrations.AlterModelTable(
            name='license',
            table='licence',
        ),
    ]