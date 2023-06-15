# Generated by Django 4.1.3 on 2022-12-06 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projecta', '0043_alter_equipmentphoto_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentphoto',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipmentphoto',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default='1970-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipmentphoto',
            name='executor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='projecta.executor', verbose_name='Исполнитель'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipmentphoto',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='equipment/'),
        ),
        migrations.AlterField(
            model_name='equipmentphoto',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='projecta.ticket', verbose_name='Заявка'),
        ),
    ]