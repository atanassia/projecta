# Generated by Django 4.1.4 on 2023-01-31 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0054_alter_actstatus_executor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1024, verbose_name='Текстовое поле')),
            ],
        ),
        migrations.CreateModel(
            name='LnsurancePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_insurance_company', models.CharField(max_length=1024, verbose_name='Страховая организация')),
                ('date_from', models.DateField(verbose_name='Дата начала')),
                ('date_to', models.DateField(verbose_name='Дата конца')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('agreement_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurances', to='projecta.agreement', verbose_name='Договор')),
                ('executor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurances', to='projecta.executor', verbose_name='Исполнитель')),
            ],
        ),
    ]