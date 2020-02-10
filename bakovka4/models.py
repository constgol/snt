from django.db import models


class Land(models.Model):
    id = models.IntegerField(verbose_name='N участка', primary_key=True)

    class Meta:
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'

    def __str__(self):
        return 'Участок № '+ str(self.id)


class PaymentChr(models.Model):
    s_pay_date   = models.CharField(max_length= 10, verbose_name='Дата оплаты'    , null=True)            # 10
    pay_date     = models.DateField(verbose_name='Дата оплаты')                                           # 10
    user_info    = models.CharField(max_length=200, verbose_name='Плательщик')
    account_info = models.CharField(max_length=100, verbose_name='Счёт'           , null=True)            # 48
    doc_num      = models.CharField(max_length= 10, verbose_name='Номер документа', null=True)            # 7
    s_amount     = models.CharField(max_length= 10, verbose_name='Сумма'          , null=True)            # 9
    amount       = models.DecimalField(max_digits= 10, decimal_places=2, verbose_name='Сумма', default=0) # 9
    type_op      = models.CharField(max_length=  2, verbose_name='Вид операции'   , null=True)            # 1
    bank_acc     = models.CharField(max_length=100, verbose_name='Банк'           , null=True)            # 65
    pay_purpose  = models.CharField(max_length=300, verbose_name='Назначение')                            # 210
    site         = models.ForeignKey(Land, verbose_name='Участок', null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Поступление'
        verbose_name_plural = 'Поступления'

    def __str__(self):
        return ''
