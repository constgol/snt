from django.db import models
from datetime import date


class PaymentChr(models.Model):
    s_pay_date   = models.CharField(max_length= 10, verbose_name='Дата оплаты')     # 10
    pay_date     = models.DateField(verbose_name='Дата оплаты')                     # 10
    user_info    = models.CharField(max_length=200, verbose_name='Плательщик')
    account_info = models.CharField(max_length=100, verbose_name='Счёт')            # 48
    doc_num      = models.CharField(max_length= 10, verbose_name='Номер документа') # 7
    s_amount     = models.CharField(max_length= 10, verbose_name='Сумма')           # 9
    amount       = models.DecimalField(max_digits= 10, decimal_places=2, verbose_name='Сумма', default=0)           # 9
    type_op      = models.CharField(max_length=  2, verbose_name='Вид операции')    # 1
    bank_acc     = models.CharField(max_length=100, verbose_name='Банк')            # 65
    pay_purpose  = models.CharField(max_length=300, verbose_name='Назначение')      # 210

    class Meta:
        verbose_name = 'Поступление'
        verbose_name_plural = 'Поступления'
