# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import json
import os
import shutil
import subprocess


directory_name = 'leases'
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

with open('info.json') as file:
    info = json.load(file)

today = datetime.today()
lease_due_date = datetime.strptime(info['Lease due date'], '%Y-%m-%d')
assert today <= lease_due_date, 'Lease due date in info.json must not be in the past'
security_deposit_due_date = datetime.strptime(info['Security deposit due date'], '%Y-%m-%d')
assert lease_due_date < security_deposit_due_date, 'Security deposit due date in info.json must be after lease due date'
lease_start_date = datetime.strptime(info['Lease start date'], '%Y-%m-%d')
assert security_deposit_due_date <= lease_start_date, 'Lease start date in info.json must be on or after security deposit due date'
assert lease_start_date < datetime.strptime(info['Lease end date'], '%Y-%m-%d'), 'Lease end date in info.json must be after start date'

with open(os.path.join('support', 'lease-info.tex'), 'w') as file:
    file.write('\\newcommand\leaseDescription{{{}}}\n'.format(info['Lease description']))
    file.write('\DTMsavedate{{lease start date}}{{{}}}\n'.format(info['Lease start date']))
    file.write('\DTMsavedate{{lease end date}}{{{}}}\n'.format(info['Lease end date']))
    file.write(
        '\\newcount\\termDuration\n'
        '\DTMsaveddatediff{lease end date}{lease start date}{\\termDuration}\n'
        '\\newcommand\\rentTable{\n'
    )
    rent_total = 0
    for monthAndRent in info['Rent']:
        file.write('{}&\\${:,.2f}\\\\\n'.format(
            datetime.strptime(monthAndRent[0], '%Y-%m').strftime('%B 15, %Y'),
            monthAndRent[1]
        ))
        rent_total += monthAndRent[1]
    file.write('}\n')
    file.write('\\newcommand\\rentTotal{{\${:,.2f}}}\n'.format(rent_total))
    file.write('\DTMsavedate{{lease due date}}{{{}}}\n'.format(info['Lease due date']))
    file.write(
        '\\newcounter{month}\n'
        '\setcounter{month}{\DTMfetchmonth{lease due date}}\n'
    )
    file.write('\\newcommand\securityDeposit{{\${:,.2f}}}\n'.format(info['Security deposit']))
    file.write('\DTMsavedate{{security deposit due date}}{{{}}}\n'.format(info['Security deposit due date']))
    file.write('\\newcommand\securityDepositLocation{{{}}}\n'.format(info['Security deposit location']))
    file.write('\\newcommand\AlumniAdvisorName{{{}}}\n'.format(info['Alumni Advisor name']))
    file.write('\\newcommand\AlumniAdvisorAddress{{{}}}\n'.format(info['Alumni Advisor address']))
    file.write('\\newcommand\SigmaSignatoryName{{{}}}\n'.format(info['Sigma signatory name']))
    file.write('\\newcommand\SigmaSignatoryTitle{{{}}}\n'.format(info['Sigma signatory title']))
    file.write('\\newcommand\SigmaSignatureDate{{{date:%B} {date.day}, {date.year}}}\n'.format(date=today))

with open('tenants.csv') as file:
    for row in csv.DictReader(file):
        tenant_first_name = row['Tenant first name'].strip()
        tenant_last_name = row['Tenant last name'].strip()

        with open(os.path.join('support', 'tenant-info.tex'), 'w') as file:
            file.write('\\newcommand\\tenantName{{{} {}}}\n'.format(tenant_first_name, tenant_last_name))
            tenant_address = row['Tenant address'].strip()
            file.write('\\newcommand\\tenantAddress{{{}}}\n'.format(tenant_address))
            file.write('\\newcommand\guarantorName{{{}}}\n'.format(row['Guarantor name'].strip()))
            guarantor_address = row['Guarantor address']
            if not guarantor_address:
                guarantor_address = tenant_address
            file.write('\\newcommand\guarantorAddress{{{}}}\n'.format(guarantor_address))

        # Run XeTeX three times so that references are correct.
        for _ in range(2):
            subprocess.check_call([
                'luatex',
                '-fmt=lualatex',
                '-interaction=batchmode',
                'Lease.tex'
            ])

        shutil.copy('Lease.pdf', os.path.join('leases', '{} {} {} Lease.pdf'.format(tenant_first_name, tenant_last_name, info['Lease description'])))
