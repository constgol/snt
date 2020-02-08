from django.contrib import admin
from .models import PaymentChr
from django import forms

class PaymentChrAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentChrAdminForm, self).__init__(*args, **kwargs)
        self.fields['user_info']   .widget = forms.Textarea(attrs = {'rows':3,'cols':150})
        self.fields['account_info'].widget = forms.Textarea(attrs = {'rows':3,'cols':150})
        self.fields['bank_acc']    .widget = forms.Textarea(attrs = {'rows':2,'cols':150})
        self.fields['pay_purpose'] .widget = forms.Textarea(attrs = {'rows':2,'cols':150})


class PaymentChrAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'site',
                'pay_date',
                'amount',
                'user_info',
                'pay_purpose',
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                's_pay_date',
                's_amount',
                'account_info',
                'doc_num',
                'type_op',
                'bank_acc',
            ),
        }),
    )
    list_display =('site', 'pay_date', 'amount', 'user_info', 'pay_purpose')
    form = PaymentChrAdminForm


admin.site.register(PaymentChr, PaymentChrAdmin)

