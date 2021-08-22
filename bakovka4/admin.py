from django import forms
from django.contrib import admin
from django.db.models import Sum
from .models import Auto
from .models import Indication
from .models import Land
from .models import Meter
from .models import PaymentChr

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
                'journal_pay_num',
                'page_num',
                'line_num',
                'site',
                'pay_date',
                'amount',
                'user_info',
                'pay_purpose',
                'purpose',
                'journal_id',
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
    list_display =('id', 'journal_id', 'journal_pay_num', 'page_num', 'line_num', 'site',
                   'pay_date', 'amount', 'user_info', 'pay_purpose', 'purpose')
    ordering = ['journal_id','id']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        print ('user:' + request.user._wrapped.get_username())

        if request.user.is_authenticated and request.user.has_perm('bakovka4.change_paymentchr'):
            self.form = PaymentChrAdminForm
        else:
            self.form = forms.ModelForm
        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
#        if request.user.is_superuser:
#            return qs
#        return qs.filter(site__in =[4,1])
        return qs


admin.site.register(PaymentChr, PaymentChrAdmin)


class PaymentChrInline(admin.TabularInline):
    model = PaymentChr
    fields = ('id', 'journal_id', 'page_num', 'line_num', 'journal_pay_num', 'pay_date', 'amount', 'user_info', 'pay_purpose', 'purpose')
    ordering = ['pay_date']
    extra = 0


class MeterInLine(admin.TabularInline):
    model = Meter
    fields = ('id', 'number', 'type')
    ordering = ['type', 'number']
    extra = 0


class AutoInLine(admin.TabularInline):
    model = Auto
    fields = ('id', 'year', 'count')
    ordering = ['year']
    extra = 0


class LandAdmin(admin.ModelAdmin):
    list_display =('id','land_total')
    ordering = ['id']

    def land_total(self, obj):
        return '{0:>10.2f}'\
            .format(PaymentChr.objects.filter(site=obj.id).aggregate(Sum('amount'))['amount__sum'])

    land_total.short_description = 'Сумма платежей'
    inlines = [MeterInLine, AutoInLine, PaymentChrInline]


admin.site.register(Land, LandAdmin)

class IndicationInLine(admin.TabularInline):
    model = Indication
    fields = ('id', 'meter', 'indic_date', 'indic_value')
    extra = 0


class MeterAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'site', 'number')
    ordering = ['type', 'site', 'number']

    inlines = [IndicationInLine]

admin.site.register(Meter, MeterAdmin)


class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'year', 'count')
    ordering = ['site', 'year']

admin.site.register(Auto, AutoAdmin)
