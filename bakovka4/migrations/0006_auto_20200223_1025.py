# Generated by Django 3.0.2 on 2020-02-23 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakovka4', '0005_auto_20200216_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentchr',
            name='purpose',
            field=models.CharField(choices=[('membership', 'членские взносы'), ('electrycity', 'электричество'), ('water', 'вода'), ('road', 'дороги'), ('truc', 'грузовой транспорт'), ('common_cadaster', 'общий кадастр'), ('common_water', 'общий водопровод'), ('common_light', 'общий свет')], max_length=50, null=True, verbose_name='Назначение'),
        ),
    ]
