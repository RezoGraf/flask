from flask import session
from unittest import result
from dateutil import parser
import app.db, app.sql


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
 
def access_user_otd(arena_user):
    result_accessotd = app.db.select(app.sql.sql_accessOtd.format(arena_user=arena_user))[0][0]
    
    if  result_accessotd != '0':
        select_otd=f' and otd in({result_accessotd})' #доступные отделения
    else:
        select_otd = ''
         
    return select_otd

def access_user_sdl(arena_user):
    result_accessSdl = app.db.select(app.sql.sql_accessSdl.format(arena_user=arena_user))[0][0]
    
    if  result_accessSdl != '0':
        select_sdl=f' and n_doc.sdl in ({result_accessSdl})' #доступные отделения
    else:
        select_sdl = ''
         
    return select_sdl


def db_to_html_table(data, **kwargs) -> String:
    print(kwargs)
    table_tr = """<tbody>"""
    x = 0
    for x in range(len(data)):
        if data[x]['CERT'] == None:
            data[x]['CERT'] = 'Отсутствует'
            table_row = f"""<tr id="{data[x]['IDW']}">
                <td>{data[x]['FAM_WORKER']} {data[x]['IM_WORKER']} {data[x]['OT_WORKER']}</td>
                <td>{data[x]['PODR']}</td>
                <td>{data[x]['OTD']}</td>
                <td>{data[x]['DLJ']}</td>
                <td>{data[x]['CERT']}</td>
                </tr>"""
            table_tr += table_row
            table_row = ''
            x += 1
    table_tr += """</tbody"""
    return table_tr