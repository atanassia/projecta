# Generated by Django 4.1.3 on 2022-12-06 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0042_equipmentphoto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentphoto',
            options={'verbose_name': 'Фото оборудования', 'verbose_name_plural': 'Фото оборудования'},
        ),
        migrations.RemoveField(
            model_name='equipmentphoto',
            name='equipment',
        ),
        migrations.AddField(
            model_name='equipmentphoto',
            name='ticket',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='projecta.ticket', verbose_name='Фото'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='equipmentphoto',
            table='equip_photo',
        ),
    ]
