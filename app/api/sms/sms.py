import db_sms
import datetime
from loguru import logger
import sql_sms
import requests
import jxmlease
import re
import time
import schedule


@logger.catch
def sms(tsms):
    """_summary_
    Returns:
        _type_: _description_
    """
    date = datetime.datetime.now()
    date_tom = date + datetime.timedelta(days=1)
    date = date.strftime('%d.%m.%Y')
    date_tom = date_tom.strftime('%d.%m.%Y')
    if tsms == 2:
        nosend_sms = db_sms.select(sql_sms.sql_sms_sel_cancel.format(date=date))
    if tsms == 1:
        nosend_sms = db_sms.select(sql_sms.sql_sms_select_1.format(date_tom=date_tom))
    if tsms == 0:
        nosend_sms = db_sms.select(sql_sms.sql_sms_select_0.format(date=date))
    print(nosend_sms)
    if nosend_sms != []:
        for i, _ in enumerate(nosend_sms):
            date = datetime.datetime.now()
            date_time = date.strftime('%d.%m.%Y %H:%M:%S')
            date = date.strftime('%d.%m.%Y')
            sms = nosend_sms[i][3]
            sms = sms.strip()
            tel = nosend_sms[i][2]
            tel = tel.strip()
            tel = tel.lstrip("+")
            uid = nosend_sms[i][0]
            uip = nosend_sms[i][1]
            db_sms.write(sql_sms.sql_sms_send.format(status=2, comment='Передано', date=date, date_time=date_time, uid=uid, uip=uip, tsms=tsms, tel=tel))
            url =f"""https://a2p-sms-https.beeline.ru/proto/http/?user=1677651&pass=Gecnjq01&action=post_sms
                    &message={sms}
                    &sender=oksp42ru
                    &target={tel}
                    &HTTP_ACCEPT_LANGUAGE=ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3"""
            response = requests.post(url)
            xml_dict = jxmlease.parse(response.content)
            xml_str = str(xml_dict)
            xml_for_db = xml_str[0:1000]
            xml_for_db = xml_for_db.replace("'", "")
            if re.search(r"errors", xml_str):
                db_sms.write(sql_sms.sql_sms_send.format(status=2, comment=xml_for_db, date=date, date_time=date_time, uid=uid, uip=uip, tsms=tsms, tel=tel))
            else:
                db_sms.write(sql_sms.sql_sms_send.format(status=1, comment='Доставлено', date=date, date_time=date_time, uid=uid, uip=uip, tsms=tsms, tel=tel))

@logger.catch
def send_sms():
    """_summary_
    Returns:
        _type_: _description_
    """
    # каждые 50 сек отправка смс о записи
    schedule.every(50).seconds.do(sms, tsms=0)
    schedule.every(55).seconds.do(sms, tsms=2)
    # каждый день в 20:20 отправка о записи на завтра
    schedule.every().day.at("20:20").do(sms, tsms=1)
    # бесконечный цикл
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    send_sms()
  