# Generated by Django 4.1.2 on 2022-11-24 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0033_remove_executor_num_reg_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreement',
            name='license',
        ),
        migrations.AddField(
            model_name='license',
            name='agreement',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='license', to='projecta.agreement', verbose_name='Договор'),
            preserve_default=False,
        ),
    ]