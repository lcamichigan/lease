#!/usr/bin/env python
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
        file.write(textwrap.dedent('''\
        {{
            "Name": "Your Name",
            "Title": "Your Title, Sigma Alumni Association",
            "Email address": "your.address@domain.com",

            "Lease description": "Fall {current_year} and Winter {next_year}",
            "Lease due date": "{current_year}-04-01",
            "Lease start date": "{current_year}-08-15",
            "Lease end date": "{next_year}-05-15",
            "Rent": [
                ["{current_year}-08-15", 740],
                ["{current_year}-09-15", 740],
                ["{current_year}-10-15", 740],
                ["{current_year}-11-15", 740],
                ["{current_year}-12-15", 740],
                ["{next_year}-01-15", 740],
                ["{next_year}-02-15", 740],
                ["{next_year}-03-15", 740],
                ["{next_year}-04-15", 740]
            ],
            "Monthly rent during holdover": 1110,

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
        )))

file_path = 'tenants.csv'
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        csv.writer(file).writerows([
            ['Tenant first name', 'Tenant last name', 'Email address', 'Tenant address', 'Is Fraternity member', 'Guarantor name', 'Guarantor address'],
            ['Tenant1FirstName', 'Tenant1LastName', 'address1@domain.com', '"Tenant1Address"', 'TRUE', 'Guarantor1Name'],
            ['Tenant2FirstName', 'Tenant2LastName', 'address2@domain.com', '"Tenant2Address"', 'TRUE', 'Guarantor2Name', '"Guarantor2Address"']
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
    subprocess.check_call([
        'lualatex',
        '-interaction=batchmode',
        '-jobname=' + jobname,
        '-output-directory=' + directory_name,
        (
            # See
            # https://tex.stackexchange.com/questions/315025/lualatex-texlive-2016-standalone-undefined-control-sequence
            # for more information about why the luatex85 package is required.
            '\RequirePackage{luatex85}'
            '\documentclass[varwidth]{standalone}'
            '\\begin{document}\sffamily '
            'Replace ' + file_path.replace('\\', '\\textbackslash ') + '\par with an image of a signature.'
            '\end{document}'
        )
    ])
