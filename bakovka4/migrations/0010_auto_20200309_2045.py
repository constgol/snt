# Generated by Django 3.0.2 on 2020-03-09 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bakovka4', '0009_auto_20200305_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentchr',
            name='journal_id',
            field=models.IntegerField(default=1, verbose_name='Номер журнала'),
        ),
        migrations.AddField(
            model_name='paymentchr',
            name='journal_pay_num',
            field=models.IntegerField(default=0, verbose_name='Номер в журнале'),
        ),
        migrations.AddField(
            model_name='paymentchr',
            name='line_num',
            field=models.IntegerField(default=1, verbose_name='Строка'),
        ),
        migrations.AddField(
            model_name='paymentchr',
            name='page_num',
            field=models.IntegerField(default=1, verbose_name='Страница'),
        ),
    ]
