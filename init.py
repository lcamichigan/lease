# -*- coding: utf-8 -*-

import csv
from datetime import date
import os
import subprocess
import textwrap

# http://docs.python-requests.org/en/master/
import requests


file_path = 'info.json'
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        current_year = date.today().year
        next_year = current_year + 1
        file.write(textwrap.dedent('''
        {{
            "Name": "Your Name",
            "Title": "Your Title, Sigma Alumni Association",
            "Email address": "your.address@domain.com",

            "Lease description": "Fall {current_year} and Winter {next_year}",
            "Lease start date": "{current_year}-08",
            "Lease end date": "{next_year}-05-15",
            "Rent": [
                ["{current_year}-08", 720],
                ["{current_year}-09", 720],
                ["{current_year}-10", 720],
                ["{current_year}-11", 720],
                ["{current_year}-12", 720],
                ["{next_year}-01", 720],
                ["{next_year}-02", 720],
                ["{next_year}-03", 720],
                ["{next_year}-04", 720]
            ],
            "Lease due date": "{current_year}-04-01",

            "Security deposit": 500,
            "Security deposit due date": "{current_year}-05-15",
            "Security deposit location": "ABC Bank, 123 Main St, Anywhere MI 00000-0000",

            "Alumni Advisor name": "John Mason",
            "Alumni Advisor email address": "alumni.advisor@domain.com",
            "Alumni Advisor address": "123 Main St, Elsewhere MI 00000-0000",

            "Sigma signatory name": "Warren Cole",
            "Sigma signatory title": "President"
        }}
        '''.format(
            current_year = current_year,
            next_year    = next_year
        )).lstrip())

file_path = 'tenants.csv'
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        csv.writer(file).writerows([
            ['Tenant first name', 'Tenant last name', 'Email address', 'Tenant address', 'Guarantor name', 'Guarantor address'],
            ['Tenant1FirstName', 'Tenant1LastName', 'address1@domain.com', '"Tenant1Address"', 'Guarantor1Name'],
            ['Tenant2FirstName', 'Tenant2LastName', 'address2@domain.com', '"Tenant2Address"', 'Guarantor2Name', '"Guarantor2Address"']
        ])

directory_name = 'support'
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

# https://www.epa.gov/lead/protect-your-family-lead-your-home-real-estate-disclosure
file_path = os.path.join(directory_name, 'lead_in_your_home_brochure_land_b_w_508_easy_print_0.pdf')
if not os.path.exists(file_path):
    with open(file_path, 'wb') as file:
        file.write(requests.get('https://www.epa.gov/sites/production/files/2014-02/documents/' + os.path.basename(file_path)).content)

# https://www.epa.gov/lead/sellers-disclosure-information-lead-based-paint-andor-lead-based-paint-hazards
file_path = os.path.join(directory_name, 'lesr_eng.pdf')
if not os.path.exists(file_path):
    with open(file_path, 'wb') as file:
        file.write(requests.get('https://www.epa.gov/sites/production/files/documents/' + os.path.basename(file_path)).content)

jobname = 'SigmaSignature'
file_path = os.path.join(directory_name, jobname + '.pdf')
if not os.path.exists(file_path):
    subprocess.check_output([
        'xetex',
        '-fmt=xelatex',
        '-interaction=batchmode',
        '-jobname=' + jobname,
        '-output-directory=' + directory_name,
        (
            '\documentclass[varwidth]{standalone}'
            '\\begin{document}\sffamily '
            'Replace ' + file_path.replace('\\', '\\textbackslash ') + '\par with an image of a signature.'
            '\end{document}'
        )
    ])
