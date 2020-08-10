import email
import getpass
import imaplib
import os
import re


def is_financial_email(payload):
    for entry in finan_email_strings:
        if entry in payload:
            return True, entry
    return False, None


def convert_to_csv():
    import csv
    toCSV = op
    keys = toCSV[0].keys()
    with open('{}/finin/transactions.csv'.format(attach_dir), 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)


def get_message_text(msg):
    payload = ''
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                payload = part.get_payload(decode=True).decode("utf-8")  # decode
                break
    else:
        payload = msg.get_payload(decode=True).decode("utf-8")
    return payload


def get_amount(payload):
    amount = ''
    try:
        amount = re.findall(r"(?:[\₹\bRs\brs]{1}[,\d]+.?\d*)")
    except Exception:
        return amount


attach_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

finan_email_strings = ['invoice', 'transaction', 'bill', 'subscription', 'debit', 'credit', 'amount']

user = input("Enter your GMail username --> ")
pwd = getpass.getpass("Enter your password --> ")
start_date = input("Enter start date in format: 01-Jan-2012 --> ")
end_date = input("Enter end date in format: 01-Jan-2012 --> ")

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(user, pwd)

mail.select()
rv, data = mail.search(None, '(SINCE "{}" BEFORE "{}")'.format(start_date, end_date))
if rv != 'OK':
    print("No messages found!")
    exit()

op = []

for num in data[0].split():
    rv, mail_data = mail.fetch(num, '(RFC822)')
    if rv != 'OK':
        print("ERROR getting message", num)
        continue
    try:
        msg = email.message_from_string(mail_data[0][1].decode('utf-8'))
    except Exception:
        continue
    payload = get_message_text(msg)
    is_finan_email, finan_email_type = is_financial_email(payload)
    if not is_finan_email:
        continue
    else:
        date = msg['Date']
    amount = get_amount(payload)
    op.append({'date': date, 'type': finan_email_type, 'amount': amount})
convert_to_csv()
