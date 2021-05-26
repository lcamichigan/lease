#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from datetime import date
import os
import subprocess
import json

# http://docs.python-requests.org/en/master/
import requests


file_path = 'info.json'
if not os.path.exists(file_path):
    current_year = date.today().year
    next_year = current_year + 1

    rent = 765

    data = {
            "Name": "Your Name",
            "Title": "Your Title, Sigma Alumni Association",
            "Email address": "your.address@domain.com",

            "Lease description": "Fall %d and Winter %d" % (current_year, next_year),
            "Lease due date": "%d-04-01" % current_year,
            "Lease start date": "%d-08-15" % current_year,
            "Lease end date": "%d-05-15" % next_year,
            "Rent": [
                ["%d-08-15" % current_year, rent],
                ["%d-09-15" % current_year, rent],
                ["%d-10-15" % current_year, rent],
                ["%d-11-15" % current_year, rent],
                ["%d-12-15" % current_year, rent],
                ["%d-01-15" % next_year, rent],
                ["%d-02-15" % next_year, rent],
                ["%d-03-15" % next_year, rent],
                ["%d-04-15" % next_year, rent]
            ],
            "Monthly rent during holdover": int(rent * 1.5),

            "Security deposit": 500,
            "Security deposit due date": "%d-05-15" % current_year,
            "Security deposit location": "ABC Bank, 123 Main St, Anywhere MI 00000-0000",

            "Alumni Advisor name": "John Mason",
            "Alumni Advisor email address": "alumni.advisor@domain.com",
            "Alumni Advisor address": "123 Main St, Elsewhere MI 00000-0000",

            "Sigma signatory name": "Warren Cole",
            "Sigma signatory title": "President"
        }

    with open(file_path, 'w') as fout:
        json.dump(data, fout, indent=4)

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
    req = requests.get('https://www.epa.gov/sites/production/files/2014-02/documents/' + os.path.basename(file_path))
    req.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(req.content)

# https://www.epa.gov/lead/sellers-disclosure-information-lead-based-paint-andor-lead-based-paint-hazards
file_path = os.path.join(directory_name, 'lesr_eng.pdf')
if not os.path.exists(file_path):
    req = requests.get('https://www.epa.gov/sites/production/files/documents/' + os.path.basename(file_path))
    req.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(req.content)

jobname = 'SigmaSignature'
file_path = os.path.join(directory_name, jobname + '.pdf')
if not os.path.exists(file_path):
    cmd = [
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
    ]

    subprocess.check_call(cmd)
