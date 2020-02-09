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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        print ('user:' + request.user._wrapped.get_username())

        if request.user.is_authenticated and request.user.has_perm('bakovka4.change_paymentchr'):
            self.form = PaymentChrAdminForm
        else:
            self.form = forms.ModelForm
        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(site__in =[4,1])


admin.site.register(PaymentChr, PaymentChrAdmin)

