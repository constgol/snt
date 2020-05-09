from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_month(value):
    res = re.match('([01][0-9])\.([0-9]{4})', value)
    if (not (res
             and 1 <= int(res.group(1)) <= 12
             and 1990 <= int(res.group(2)) <= 2030)):
        raise ValidationError(
            _('%(value) - месяц должен быть формате "MM.YYYY"'),
            params={'value': value},
        )


class Land(models.Model):
    id = models.IntegerField(verbose_name='N участка', primary_key=True)
    memb_from = models.CharField(max_length=7, verbose_name='Взносы с месяца',
                                 validators=[validate_month], default='06.2014')
    memb_to = models.CharField(max_length=7, verbose_name='Взносы по месяц',
                               validators=[validate_month], default='03.2020')

    class Meta:
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'

    def __str__(self):
        return 'Участок № ' + str(self.id)


PAYMENT_PURPOSE = [
    ('membership', 'Членские взносы'),
    ('electrycity', 'Электричество'),
    ('water', 'Вода'),
    ('road', 'Дороги'),
    ('truc', 'Грузовой транспорт'),
    ('common_cadaster', 'Общий кадастр'),
    ('common_water', 'Общий водопровод'),
    ('common_light', 'Общий свет'),
]


class PaymentChr(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    s_pay_date = models.CharField(max_length=10, verbose_name='Дата оплаты', blank=True, default='')  # 10
    pay_date = models.DateField(verbose_name='Дата оплаты')  # 10
    user_info = models.CharField(max_length=200, verbose_name='Плательщик')
    account_info = models.CharField(max_length=100, verbose_name='Счёт', blank=True, default='')  # 48
    doc_num = models.CharField(max_length=10, verbose_name='Номер документа', blank=True, default='')  # 7
    s_amount = models.CharField(max_length=10, verbose_name='Сумма', blank=True, default='')  # 9
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма', default=0)  # 9
    type_op = models.CharField(max_length=2, verbose_name='Вид операции', blank=True, default='')  # 1
    bank_acc = models.CharField(max_length=100, verbose_name='Банк', blank=True, default='')  # 65
    pay_purpose = models.CharField(max_length=300, verbose_name='Описание платежа')  # 210
    site = models.ForeignKey(Land, verbose_name='Участок', on_delete=models.PROTECT, null=True)
    purpose = models.CharField(max_length=50, verbose_name='Назначение', choices=PAYMENT_PURPOSE, blank=True,
                               default='')
    parent_pay_id = models.ForeignKey('self', verbose_name='Из платежа', on_delete=models.PROTECT, null=True)
    journal_id = models.IntegerField(verbose_name = 'Номер журнала', default=1)
    journal_pay_num = models.IntegerField(verbose_name='Номер в журнале', default=0)
    page_num = models.IntegerField(verbose_name='Страница', default=1)
    line_num = models.IntegerField(verbose_name='Строка', default=1)

    class Meta:
        verbose_name = 'Поступление'
        verbose_name_plural = 'Поступления'

    def __str__(self):
        return ''

METER_TYPE = [
    ('electrycity', 'Электричество'),
    ('water', 'Вода'),
]

class Meter(models.Model):
     site = models.ForeignKey(Land, verbose_name='Участок', on_delete=models.PROTECT, null=True)
     number = models.CharField(max_length=100, verbose_name='Номер счетчика', blank=True, default='')
     type = models.CharField(max_length=50, verbose_name='Тип счетчика', choices=METER_TYPE, blank=True, default='')

     class Meta:
         verbose_name = 'Счетчик'
         verbose_name_plural = 'Счетчики'

     def __str__(self):
         return self.number

class Indication(models.Model):
    meter = models.ForeignKey(Meter, verbose_name='Счетчик', on_delete=models.PROTECT, null=True)
    indic_date = models.DateField(verbose_name='Дата показания')
    indic_value = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Показание', default=0)

    class Meta:
        verbose_name = 'Показание'
        verbose_name_plural = 'Показания'
