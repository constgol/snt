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
    list_display =('pay_date', 'user_info', 'amount', 'pay_purpose')
    form = PaymentChrAdminForm


admin.site.register(PaymentChr, PaymentChrAdmin)

