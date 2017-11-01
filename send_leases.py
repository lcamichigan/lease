# -*- coding: utf-8 -*-

import csv
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import json
import os
import smtplib
import sys
import textwrap


with open('info.json') as file:
    info = json.load(file)

date_template = '{date:%B} {date.day}, {date.year}'
lease_start_date = date_template.format(date=datetime.strptime(info['Lease start date'] + '-15', '%Y-%m-%d'))
security_deposit_due_date = datetime.strptime(info['Security deposit due date'], '%Y-%m-%d')

message_template = '''{{tenant_first_name}},

Please find attached your lease for {lease_description}, a copy of the EPA’s pamphlet “Protect Your Family From Lead in Your Home”, and a move-in form.

Before signing the lease, you and {{guarantor_name}} (your guarantor) should read it carefully. To avoid late fees and ensure you’ll be able to move in on {lease_start_date}, here are a few things you must do:

1. Deliver your signed lease to High Pi {Alumni_Advisor_name} by {lease_due_date}. You and your guarantor must sign the signature page. In addition, please remember to initial items (c) and (d) of and sign the Disclosure of Information on Lead-Based Paint form on the last page of the lease.

2. If this will be your first time living in the chapter house, on {security_deposit_invoice_date} you’ll be emailed an invoice for your ${security_deposit} security deposit. Please pay this invoice by {security_deposit_due_date}. If you’ve lived in the chapter house before, we’ll apply your previous security deposit to this lease.

3. On {first_rent_invoice_date} you’ll be emailed an invoice for your first month’s rent. Please pay this invoice by {lease_start_date}.

Please let me know if you have any questions.

{name}
{title}

'''.format(
    lease_description             = info['Lease description'].lower(),
    lease_start_date              = lease_start_date,
    Alumni_Advisor_name           = info['Alumni Advisor name'],
    lease_due_date                = date_template.format(date=datetime.strptime(info['Lease due date'], '%Y-%m-%d')),
    security_deposit_invoice_date = security_deposit_due_date.strftime('%B 1, %Y'),
    security_deposit              = '{:,.2f}'.format(info['Security deposit']),
    security_deposit_due_date     = date_template.format(date=security_deposit_due_date),
    first_rent_invoice_date       = datetime.strptime(info['Lease start date'], '%Y-%m').strftime('%B 1, %Y'),
    name                          = info['Name'],
    title                         = info['Title']
)

common_attachments = []
for path in [os.path.join('support', 'lead_in_your_home_brochure_land_b_w_508_easy_print_0.pdf'), 'Move-In Form.rtf']:
    with open(path, 'rb') as file:
        attachment = MIMEApplication(file.read(), _subtype=os.path.splitext(path))
    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
    common_attachments.append(attachment)

email_address = info['Email address'];
if 'SMTP host' in info and 'SMTP port' in info:
    SMTP_host = info['SMTP host']
    SMTP_port = info['SMTP port']
else:
    email_domain = email_address.partition('@')[2].lower()
    if 'gmail.com' == email_domain:
        # https://support.google.com/mail/answer/7126229
        SMTP_host = info.get('SMTP host', 'smtp.gmail.com')
        SMTP_port = info.get('SMTP port', 587)
    elif 'outlook.com' == email_domain:
        # https://support.office.com/en-us/article/POP-IMAP-and-SMTP-settings-for-Outlook-com-d088b986-291d-42b8-9564-9c414e2aa040
        SMTP_host = info.get('SMTP host', 'smtp-mail.outlook.com')
        SMTP_port = info.get('SMTP port', 587)
    elif 'yahoo.com' == email_domain:
        # https://help.yahoo.com/kb/SLN4724.html
        SMTP_host = info.get('SMTP host', 'smtp.mail.yahoo.com')
        SMTP_port = info.get('SMTP port', 587)
    elif 'aol.com' == email_domain:
        # https://help.aol.com/articles/how-do-i-use-other-email-applications-to-send-and-receive-my-aol-mail
        SMTP_host = info.get('SMTP host', 'smtp.aol.com')
        SMTP_port = info.get('SMTP port', 465)
    elif 'umich.edu' == email_domain:
        # http://documentation.its.umich.edu/node/309
        SMTP_host = info.get('SMTP host', 'smtp.mail.umich.edu')
        SMTP_port = info.get('SMTP port', 587)
    else:
        sys.exit(textwrap.dedent('''
            To send leases, add an SMTP host and port to info.json, like this:

                "Email address": "{}",
                "SMTP host": "<SMTP host>",
                "SMTP port": <SMTP port>,

            Replace <SMTP host> with an SMTP host (possibly smtp.{}).
            Replace <SMTP port> with a port number (probably 587).
            Look in the documentation of your email provider for this information.
        '''.format(email_address, email_domain)))

server = smtplib.SMTP(SMTP_host, SMTP_port)
server.starttls()
server.login(email_address, getpass.getpass())

with open('tenants.csv') as csv_file:
    for row in csv.DictReader(csv_file):
        tenant_first_name = row['Tenant first name'].strip()
        tenant_last_name = row['Tenant last name'].strip()

        message = MIMEMultipart()
        message['From'] = info['Email address']
        message['To'] = row['Email address']
        message['Cc'] = info['Alumni Advisor email address']
        message['Subject'] = 'Sigma {} Lease'.format(info['Lease description'])
        message.attach(MIMEText(message_template.format(
            tenant_first_name = tenant_first_name,
            guarantor_name    = row['Guarantor name'].strip()
        ), 'plain'))

        path = os.path.join('leases', '{} {} {} Lease.pdf'.format(tenant_first_name, tenant_last_name, info['Lease description']))
        with open(path, 'rb') as attached_file:
            attachment = MIMEApplication(attached_file.read(), _subtype=os.path.splitext(path))
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
        message.attach(attachment)

        for attachment in common_attachments:
            message.attach(attachment)

        server.sendmail(message['From'], message['To'], message.as_string())

server.quit()
