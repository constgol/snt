from django.shortcuts import render
from django.contrib import admin
from django.db.models import Sum
from .models import PaymentChr
from .models import PAYMENT_PURPOSE

def index(request):
    p_list = dict(PAYMENT_PURPOSE)
    p_list[''] = '-'
    purpose_list = PaymentChr.objects.values('purpose').annotate(total= Sum('amount'))
#    purpose_list = PaymentChr.objects.values ('purpose', purpose_year=Extract('pay_date', 'year')).annotate(total= Sum('amount'))
    pp = {}
    total = 0
    for row in purpose_list:
        pp[row['purpose']] = {
            'name' : p_list[row['purpose']],
            'total': '{0:>10.2f}'.format(row['total']),
        }
        total += row['total']
    ba = admin.site
    ba._build_app_dict(request)
    app_label = 'bakovka4'
    app_dict = ba._build_app_dict(request, app_label)
    context = {
        **ba.each_context(request),
        'app_list' : [app_dict],
        'app_label': app_label,
        'purpose_list': pp.items(),
        'total': '{0:>10.2f}'.format(total),
        'title': 'Назначение платежа',
         **({}),
    }
    return render(request, 'bakovka4/purpose.html', context)
