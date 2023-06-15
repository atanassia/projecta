# Generated by Django 4.1.2 on 2022-10-18 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0003_alter_clientcontact_client_alter_act_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='created',
            field=models.DateField(auto_now=True, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='act',
            name='status',
            field=models.CharField(choices=[('Без статуса', 'Без статуса'), ('У клиента', 'У клиента'), ('Подписан', 'Подписан'), ('ЭДО', 'ЭДО')], default='Без статуса', max_length=255, verbose_name='Статус'),
        ),
    ]