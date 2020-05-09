from bakovka4.models import Land
from bakovka4.models import Meter
from bakovka4.models import Indication
import csv
import datetime

with open ('data/water_meter_202005.csv', 'rt') as fin:
    cin = csv.reader(fin)
    indics = list(cin)

log_name = 'import_watermeter.py_log_' + datetime.datetime.now().strftime ('%Y%m%d_%H%M%S')  
fo = open ( 'logs/' + log_name , 'w' )
for indic in indics:
    if (indic[1] != '0'):
        fo.write ('{0:5s} {1:20s} {2:20s}\n'.format(indic[0], indic[1], indic[2]))
        met = Meter (
            number = indic[1],
            type = 'water',
        )
        if (indic[0] != '' ):
            met.site = Land.objects.filter (id = int(indic[0]))[0]
        indic = Indication (
            meter = met,
            indic_date = datetime.datetime.strptime('06.05.2020', '%d.%m.%Y').date(),
            indic_value = indic[2],
        )
        met.save()
        indic.save()

fo.close()
