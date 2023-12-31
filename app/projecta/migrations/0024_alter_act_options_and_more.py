# Generated by Django 4.1.2 on 2022-11-10 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0023_alter_act_act_status_alter_act_check_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='act',
            options={'ordering': ('-act_date', '-created'), 'verbose_name': 'Акт', 'verbose_name_plural': 'Акты'},
        ),
        migrations.AlterField(
            model_name='agreement',
            name='date_reg_certificate',
            field=models.DateField(blank=True, null=True, verbose_name='Дата регистрации'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(choices=[('ТО', 'ТО'), ('Инцидент', 'Инцидент'), ('Ремонт', 'Ремонт'), ('Замена', 'Замена'), ('Установка', 'Установка')], default='Нет типа', max_length=255, verbose_name='Тип'),
        ),
    ]
