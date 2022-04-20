#!/usr/bin/python
import psycopg2
import select
import psycopg2.extensions
import argparse, sys
import smtplib, ssl

port = 465
smtp_server = 'smtp.gmail.com'
sender_email = 'emailSendingTask@gmail.com'
receiver_email = 'magister47ludi@gmail.com'

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--port')
parser.add_argument('--dbname')
parser.add_argument('--password')
parser.add_argument('--user')
parser.add_argument('--email_password')

args = parser.parse_args()

message = """ {} attempted do delete rows in important table """

def send_email(user):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, args.email_password)
        server.sendmail(sender_email, receiver_email, message.format(user))

def connect():
    conn = None
    try:
        conn = psycopg2.connect(
                     host = args.host,
                     database = args.dbname,
                     user = args.user,
                     password = args.password,
                     port = args.port
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()
        cur.execute('listen important_ch;');

        while True:
                if select.select([conn], [], [], 5) == ([],[],[]):
                        print('waiting')
                else:
                        conn.poll()
                        while conn.notifies:
                                notify = conn.notifies.pop(0)
                                send_email(notify.payload)

    except (Exception, psycopg2.DatabaseError) as error:
        print('Exception: ')
        print(error)
    finally:
        if conn is not None:
                conn.close()

if __name__ == '__main__':
        connect()