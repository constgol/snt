var charges = [
    { year: "2012", month: "01", amount:  600 },
    { year: "2015", month: "07", amount:  800 },
    { year: "2017", month: "06", amount:  850 },
    { year: "2019", month: "06", amount: 1000 }
];

function chMonth (input_id, mm) {
    elem = document.getElementById(input_id);
    m = elem.value.match (/^(.{2})\.(.{4})$/);
    m1 = addMonth ( m[1], m[2], mm);
    elem.value =  m1.month + "." + m1.year;
}


function countCharge(start, end) {
    var st_parsed = start.match (/^(.{2})\.(.{4})$/);
    var en_parsed = end.match   (/^(.{2})\.(.{4})$/);
    st = { year: st_parsed[2], month: st_parsed[1] };
    en = { year: en_parsed[2], month: en_parsed[1] };

    a = "";
    b = "";
    total = 0;
    prev  = 0;
    br = 0;
    var prev, pyear, pmonth, tot;
    for (i=0; i < charges.length; i++) {
        b += "<tr><td>" + charges[i].month + '.' + charges[i].year + "</td><td style='text-align: right'>" + charges[i].amount + "</td></tr>";
        if (a === "") {
            pyear  = st.year;
            pmonth = st.month;
            if ( monthsBetween ( st, charges[i] ) <= 1 ) {
                prev = charges[i].amount;
                continue;
            }
            else {
                a += "<td>" + pmonth + '.' + pyear + "</td>";
            }
        }
        cur1 = addMonth (charges[i].month, charges[i].year, -1);
        if ( monthsBetween ( cur1, en ) <= 1 ) {
        cur1.year  = en.year;
	    cur1.month = en.month;
        br = 1;
    }
    mb = monthsBetween ( { year: pyear, month: pmonth }, cur1 );
    tot = prev * mb;
        total += tot;
         a += "<td>" + cur1.month + '.' + cur1.year +
             "</td><td>" + mb +
             "</td><td style='text-align: right'>" + prev +
             "</td><td style='text-align: right'>" + tot +
             "</td>";
         if ( br == 1 ){
             break;
         }
         a += "</tr><tr><td>" + charges[i].month + '.' + charges[i].year + "</td>";
         prev   = charges[i].amount;
         pyear  = charges[i].year;
         pmonth = charges[i].month;
    }
    dmonth = en.month;
    dyear  = en.year;
    mb = monthsBetween (
        { year: pyear, month: pmonth },
        { year: dyear, month: dmonth }
    );
    if ( mb >= 1 && br == 0 ) {
        tot = prev * mb;
        total += tot;
        if (a === "") {
            a += "<td>" + pmonth + '.' + pyear + "</td>";
        }
        a += "<td>" + ("000"+ dmonth).slice(-2) + '.' + dyear +
            "</td><td>" + mb +
            "</td><td style='text-align: right'>" + prev +
            "</td><td style='text-align: right'>" + tot + "</td>";
    }
//    document.getElementById("months").innerHTML = "<table>" + b + "</table>";
    document.getElementById("intervals").innerHTML = "<table><thead>" +
    "<tr><th colspan=2>Период</th><th>Месяцев</th><th>За месяц</th><th>Всего</th></tr></thead>" +
    "<tbody><tr>" + a + "</tr></tbody><tr>" +
        "<td style='text-align: left;'>Итого</td><td></td><td></td><td></td><td style='text-align: right'> " + total + "</td></tr></table>";
}

function addMonth (month, year, months) {
    var d = new Date( parseInt (year), parseInt (month)-1, 1);
    d.setMonth (d.getMonth() + months);
    return { year: d.getFullYear().toString(), month: ("000"+ (d.getMonth()+1).toString()).slice(-2) };
}

function monthsBetween (fd, td) {
    d1 = new Date ( parseInt(fd.year), parseInt(fd.month)-1, 1);
    d2 = new Date ( parseInt(td.year), parseInt(td.month)-1, 1);
    months = (d2.getFullYear() - d1.getFullYear()) * 12
        + d2.getMonth() - d1.getMonth() + 1;
    return months;
}
