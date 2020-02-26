from django.shortcuts import render
from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Extract
from .models import PaymentChr
from .models import PAYMENT_PURPOSE


def purposeIndex(request):
    p_list = dict(PAYMENT_PURPOSE)
    p_list[''] = '-'
    purpose_list = PaymentChr.objects. \
        exclude(site=None). \
        values('purpose', purpose_year=Extract('pay_date', 'year')). \
        annotate(total=Sum('amount'))
    pp = {}
    total = 0
    yp = {}
    for row in purpose_list:
        if row['purpose'] in pp:
            pp[row['purpose']]['total'] += row['total']
            pp[row['purpose']]['purpose_year'][row['purpose_year']] = row['total']
        else:
            pp[row['purpose']] = {
                'name': p_list[row['purpose']],
                'total': row['total'],
                'purpose_year': {
                    row['purpose_year']: row['total']
                }
            }

        if row['purpose_year'] in yp:
            yp[row['purpose_year']] += row['total']
        else:
            yp[row['purpose_year']] = row['total']
        total += row['total']

    years = list(yp.keys())
    years.sort()

    ba = admin.site
    ba._build_app_dict(request)
    app_label = 'bakovka4'
    app_dict = ba._build_app_dict(request, app_label)
    context = {
        **ba.each_context(request),
        'app_list': [app_dict],
        'app_label': app_label,
        'purpose_list': pp.items(),
        'total': total,
        'title': 'Назначение платежа',
        'years': years,
        'years_list': yp.items(),
        **({}),
    }
    return render(request, 'bakovka4/purpose_index.html', context)


def purposeByYear(request, purpose):
    p_list = dict(PAYMENT_PURPOSE)
    ba = admin.site
    ba._build_app_dict(request)
    app_label = 'bakovka4'
    app_dict = ba._build_app_dict(request, app_label)
    context = {
        **ba.each_context(request),
        'app_list': [app_dict],
        'app_label': app_label,
        'purpose': purpose,
        'purpose_name': p_list[purpose],
        'title': 'Назначение платежа',
    }
    return render(request, 'bakovka4/purpose_by_year.html', context)


def purposeByMonth(request, purpose, year):
    p_list = dict(PAYMENT_PURPOSE)
    ba = admin.site
    ba._build_app_dict(request)
    app_label = 'bakovka4'
    app_dict = ba._build_app_dict(request, app_label)
    context = {
        **ba.each_context(request),
        'app_list': [app_dict],
        'app_label': app_label,
        'purpose': purpose,
        'purpose_name': p_list[purpose],
        'year': year,
        'title': 'Назначение платежа',
    }
    return render(request, 'bakovka4/purpose_by_month.html', context)
