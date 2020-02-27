from django.shortcuts import render
from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Extract
from .models import PaymentChr
from .models import PAYMENT_PURPOSE
from datetime import date


def purposeIndex(request):
    p_list = dict(PAYMENT_PURPOSE)
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
    purpose_list = PaymentChr.objects. \
        exclude(site=None). \
        filter(purpose=purpose). \
        values('site', purpose_year=Extract('pay_date', 'year')). \
        annotate(total=Sum('amount'))
    pp = {}
    total = 0
    yp = {}
    for row in purpose_list:
        if row['site'] in pp:
            pp[row['site']]['total'] += row['total']
            pp[row['site']]['purpose_year'][row['purpose_year']] = row['total']
        else:
            pp[row['site']] = {
                'name': row['site'],
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
        'purpose': purpose,
        'purpose_list': pp.items(),
        'purpose_name': p_list[purpose],
        'total': total,
        'title': p_list[purpose],
        'years': years,
        'years_list': yp.items(),
        **({}),
    }
    return render(request, 'bakovka4/purpose_by_year.html', context)


def purposeByMonth(request, purpose, year):
    p_list = dict(PAYMENT_PURPOSE)
    purpose_list = PaymentChr.objects. \
        exclude(site=None). \
        filter(purpose=purpose). \
        filter(pay_date__year=year). \
        values('site', purpose_month=Extract('pay_date', 'month')). \
        annotate(total=Sum('amount'))
    pp = {}
    total = 0
    mp = {}
    for row in purpose_list:
        if row['site'] in pp:
            pp[row['site']]['total'] += row['total']
            pp[row['site']]['purpose_month'][row['purpose_month']] = row['total']
        else:
            pp[row['site']] = {
                'name': row['site'],
                'total': row['total'],
                'purpose_month': {
                    row['purpose_month']: row['total']
                }
            }

        if row['purpose_month'] in mp:
            mp[row['purpose_month']] += row['total']
        else:
            mp[row['purpose_month']] = row['total']
        total += row['total']

    months = list(range(1, 13))
    m_list = []
    for m in months:
        m_list.append(date(2020, m, 1))

    ba = admin.site
    ba._build_app_dict(request)
    app_label = 'bakovka4'
    app_dict = ba._build_app_dict(request, app_label)
    context = {
        **ba.each_context(request),
        'app_list': [app_dict],
        'app_label': app_label,
        'purpose': purpose,
        'purpose_list': pp.items(),
        'purpose_name': p_list[purpose],
        'year': year,
        'total': total,
        'title': p_list[purpose] + ' (' + str(year) + ')',
        'months': months,
        'months_list': mp,
        'm_list': m_list,
    }
    return render(request, 'bakovka4/purpose_by_month.html', context)
