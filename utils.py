# def list_to_int(list_result):
#     for s in list_result:
#         string_result = ''.join(str(e) for e in list_result)
#         string_result = string_result.replace('(', '')
#         string_result = string_result.replace(')', '')
#         string_result = string_result.replace(',', '')
#         string_result = int(string_result)
#         #string_result = string_result.append(s)
#     return string_results


from unittest import result
from dateutil import parser

def list_to_int(list_result):
    string_result = ''.join(str(e) for e in list_result)
    string_result = string_result.replace('(', '')
    string_result = string_result.replace(')', '')
    string_result = string_result.replace(',', '')
    string_result = int(string_result)
    #string_result = string_result.append(s)
    return string_result


def list_to_str(list_result):
    string_result = ''.join(str(e) for e in list_result)
    string_result = string_result.replace('(', '')
    string_result = string_result.replace(')', '')
    string_result = string_result.replace(',', '')
    string_result = string_result.replace("'", '')
    #string_result = string_result.append(s)
    return string_result

def russianNameDayWeek(day_week):
    russianDayWeek = {'Mon':'Пн.' , 'Tue':'Вт.' , 'Wed':'Ср.' , 'Thu':'Чт.' , 'Fri':'Пт.' , 'Sat':'Сб.' , 'Sun':'Вс.'}
    latin_name_dayweek = parser.parse(day_week).strftime("%a")
    result = russianDayWeek[latin_name_dayweek]
    print(day_week)
    print(latin_name_dayweek)
    return result
    
def date_color(current_date):
    dt = parser.parse(current_date)
    current_day = parser.parse(dt.strftime('%m/%d/%y')).strftime("%d")
    current_year = parser.parse(dt.strftime('%m/%d/%y')).strftime("%Y")
    current_month = parser.parse(dt.strftime('%m/%d/%y')).strftime("%m")   
    russianDayWeek = {'Mon':'Пн.' , 'Tue':'Вт.' , 'Wed':'Ср.' , 'Thu':'Чт.' , 'Fri':'Пт.' , 'Sat':'Сб.' , 'Sun':'Вс.'}
    dt = f'{str(current_day)}.{str(current_month)}.{str(current_year)}'
    ans = parser.parse(dt).strftime("%a")
    pa = russianDayWeek[ans]
    if pa == 'Вс.' :
        result = 'table-success'
    else:
        result = 'table-light'
    if pa == 'Сб.' :
        result = 'table-success'    
    return result 
    