# Generated by Django 4.1.2 on 2022-11-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0025_alter_agreement_date_reg_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='date_reg_certificate',
            field=models.DateField(blank=True, null=True, verbose_name='Дата регистрации'),
        ),
    ]
