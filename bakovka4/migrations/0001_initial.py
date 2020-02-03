# Generated by Django 3.0.2 on 2020-02-03 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentChr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_pay_date', models.CharField(max_length=10, verbose_name='Дата оплаты')),
                ('pay_date', models.DateField(verbose_name='Дата оплаты')),
                ('user_info', models.CharField(max_length=200, verbose_name='Плательщик')),
                ('account_info', models.CharField(max_length=100, verbose_name='Счёт')),
                ('doc_num', models.CharField(max_length=10, verbose_name='Номер документа')),
                ('s_amount', models.CharField(max_length=10, verbose_name='Сумма')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма')),
                ('type_op', models.CharField(max_length=2, verbose_name='Вид операции')),
                ('bank_acc', models.CharField(max_length=100, verbose_name='Банк')),
                ('pay_purpose', models.CharField(max_length=300, verbose_name='Назначение')),
            ],
            options={
                'verbose_name': 'Поступление',
                'verbose_name_plural': 'Поступления',
            },
        ),
    ]
