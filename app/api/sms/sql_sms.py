# api/sms.py-----------------------------------------
sql_sms_select_0 = """Select sms_send.UID,sms_send.UIP,sms_send.NTEL,sms_send.SMS_TXT,sms_send.DOTP from SMS_SEND,pspo_s
                    Where sms_send.status=0 and (pspo_s.uip=sms_send.uip)
                    and (pspo_s.uid=sms_send.uid)
                    and (CHAR_LENGTH(sms_send.sms_txt)>0)
                    and (CHAR_LENGTH(TRIM(sms_send.ntel))=12)
                    and (sms_send.dotp='{date}' and (sms_send.tsms=0))"""
sql_sms_select_1 = """Select sms_send.UID,sms_send.UIP,sms_send.NTEL,sms_send.SMS_TXT,sms_send.DOTP from SMS_SEND,pspo_s
                    Where sms_send.status=0 and (pspo_s.uip=sms_send.uip)
                    and (pspo_s.uid=sms_send.uid)
                    and (CHAR_LENGTH(sms_send.sms_txt)>0)
                    and (CHAR_LENGTH(TRIM(sms_send.ntel))=12)
                    and (sms_send.dv='{date_tom}' and (sms_send.tsms=1))"""
sql_sms_sel_cancel = """Select sms_send.UID,sms_send.UIP,sms_send.NTEL,sms_send.SMS_TXT,sms_send.DOTP from SMS_SEND
                        Where sms_send.status=0
                        and (CHAR_LENGTH(sms_send.sms_txt)>0)
                        and (CHAR_LENGTH(TRIM(sms_send.ntel))=12)
                        and (sms_send.dotp='{date}' and (sms_send.tsms=2))"""
sql_sms_send = """UPDATE SMS_SEND SET STATUS={status},COMMENT='{comment}',DATE_OPERATOR='{date}',DATETIME_OPERATOR='{date_time}'
                WHERE UID={uid} and UIP={uip} and TSMS={tsms} and NTEL='+{tel}'"""
