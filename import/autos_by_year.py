from bakovka4.models import Auto
from bakovka4.models import Land
import datetime

years = [
    '2014',
    '2015',
    '2016',
    '2017',
    '2018',
    '2019',
    '2020',
]

log_name = 'import/logs/import_watermeter.py_log_' + datetime.datetime.now().strftime ('%Y%m%d_%H%M%S')
print (log_name)
fo = open ( log_name , 'w', encoding='utf-8')
for land in Land.objects.all():
    fo.write (str(land) + ':')
    for y in years:
        fo.write (' '  + y)
        auto = Auto (
            site = land,
            year = y,
            count = 0
        )
        auto.save()
    fo.write('\n')

fo.close()
