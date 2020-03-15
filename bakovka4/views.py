from django.shortcuts import render
from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Extract
from .models import PaymentChr
from .models import Land
from .models import PAYMENT_PURPOSE
from datetime import date
import re

charges = [
    {'year': "2012", 'month': "01", 'amount': 600},
    {'year': "2015", 'month': "07", 'amount': 800},
    {'year': "2017", 'month': "06", 'amount': 850},
    {'year': "2019", 'month': "06", 'amount': 1000}
]

mon_year = re.compile('^(.{2})\.(.{4})$')


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
    tot_dcp = 0
    tot_dcm = 0
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

    cred = "#ff0000"
    cgreen = "#008000"
    for p in pp.values():
        land = Land.objects.filter(id=p['name']).first()
        fr_pars = mon_year.match(land.memb_from)
        to_pars = mon_year.match(land.memb_to)
        fr = {'month': fr_pars.group(1), 'year': fr_pars.group(2)}
        to = {'month': to_pars.group(1), 'year': to_pars.group(2)}
        charge_sum = calcCharge(fr, to)
        dcp = p['total'] - charge_sum
        p['memb_from'] = land.memb_from
        p['memb_to'] = land.memb_to
        p['charge_sum'] = charge_sum
        p['debt_calc_period'] = dcp
        if dcp >= 0:
            p['cp_col'] = cgreen
        else:
            p['cp_col'] = cred
        tot_dcp += dcp

        cdate = {'month': date.today().month, 'year': date.today().year}
        if (monthsBetween(to, cdate) > 1):
            p['cm_col'] = cred
            to1 = addMonth(to, 1)
            dcm = (- calcCharge(to1, cdate))
        else:
            p['cm_col'] = cgreen
            cur1 = addMonth(cdate, 1)
            dcm = (calcCharge(cur1, to))
        p['debt_cur_month'] = dcm
        tot_dcm += dcm

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
        'tot_dcp': tot_dcp,
        'tot_dcm': tot_dcm,
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


def purposeByLand(request, purpose, year, land):
    p_list = dict(PAYMENT_PURPOSE)
    l = Land.objects.filter(id=land).first()
    if (year == '-'):
        purpose_list = PaymentChr.objects. \
            filter(site=land). \
            filter(purpose=purpose). \
            order_by('pay_date'). \
            values('id', 'pay_date', 'pay_purpose', 'amount')
    else:
        purpose_list = PaymentChr.objects. \
            filter(site=land). \
            filter(purpose=purpose). \
            filter(pay_date__year=year). \
            order_by('pay_date'). \
            values('id', 'pay_date', 'pay_purpose', 'amount')

    total = 0
    for payment in purpose_list:
        total += payment['amount']
    ba = admin.site
    ba._build_app_dict(request)
    app_label = 'bakovka4'
    app_dict = ba._build_app_dict(request, app_label)
    context = {
        **ba.each_context(request),
        'app_list': [app_dict],
        'app_label': app_label,
        'purpose': purpose,
        'purpose_list': purpose_list,
        'purpose_name': p_list[purpose],
        'year': year,
        'total': total,
        'title': p_list[purpose] + ' / Участок ' + str(land),
        'land': land,
        'memb_from': l.memb_from,
        'memb_to': l.memb_to,
    }
    if year != '-':
        context['title'] += ' (' + str(year) + ')'
    return render(request, 'bakovka4/purpose_by_land.html', context)


def journal(request, journal=1, page=1):
    ba = admin.site
    ba._build_app_dict(request)
    app_label = 'bakovka4'
    app_dict = ba._build_app_dict(request, app_label)
    journals = PaymentChr.objects.values('journal_id').order_by('journal_id').distinct()
    pages = PaymentChr.objects.filter(journal_id=journal).values('page_num').order_by('page_num').distinct()
    page_line = PaymentChr.objects.filter(journal_id=journal).filter(page_num=page).order_by('pay_date', 'journal_pay_num', 'line_num')
    page_sum = PaymentChr.objects.filter(journal_id=journal).filter(page_num=page).aggregate(Sum('amount'))
    context = {
        **ba.each_context(request),
        'app_list': [app_dict],
        'app_label': app_label,
        'journal': journal,
        'journals': journals,
        'page': page,
        'page_line': page_line,
        'page_sum': page_sum['amount__sum'],
        'pages': pages,
        'title': 'Журнал ' + str(journal) + ' / Страница ' + str(page),
    }
    return render(request, 'bakovka4/journal.html', context)


def calcCharge(st, en):
    total = 0
    prev = 0
    found = False
    br = False
    pdate = {}
    for charge in charges:
        if (not found):
            pdate = st
            if (monthsBetween(st, charge) <= 1):
                prev = charge['amount']
                continue
            else:
                found = True
        cur1 = addMonth(charge, -1)
        if (monthsBetween(cur1, en) <= 1):
            cur1 = en
            br = True
        mb = monthsBetween(pdate, cur1)
        tot = prev * mb
        total += tot
        if (br):
            break
        prev = charge['amount']
        pdate = charge
    ddate = en
    mb = monthsBetween(pdate, ddate)
    if (mb >= 1 and not br):
        tot = prev * mb
        total += tot

    return total


def monthsBetween(start, end):
    return (int(end['year']) - int(start['year'])) * 12 + int(end['month']) - int(start['month']) + 1


def addMonth(start, months):
    month = int(start['month']) + months - 1
    year = int(start['year']) + month // 12
    month = month % 12 + 1
    return {'year': year, 'month': month}
