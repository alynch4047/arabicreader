

import logging
import smtplib

l = logging.getLogger(__name__)

def send_email(email_address, message, title):
    l.debug('sending %s\n________________\n%s to %s', title, message, email_address)
    try:
        headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % \
                ('abdulhaq@arabicreader.net', email_address, title)
        
        server = smtplib.SMTP('localhost', timeout=2)
        server.set_debuglevel(0)
        server.sendmail('abdulhaq@arabicreader.net',
                        [email_address, 'alynch4047@gmail.com'],
                         headers + message)
        server.quit()
    except Exception as ex:
        l.exception('cant send email (%s)', ex)
