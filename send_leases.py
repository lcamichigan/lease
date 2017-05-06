# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import getpass
import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib


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

server = smtplib.SMTP(info['SMTP host'], info['SMTP port'])
server.starttls()
server.login(info['Email address'], getpass.getpass())

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
