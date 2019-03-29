# Lease

[![Build status](https://ci.appveyor.com/api/projects/status/30r7r9c9uwue29cg?svg=true)](https://ci.appveyor.com/project/lcamichigan/lease)
[![Build Status](https://travis-ci.org/lcamichigan/lease.svg?branch=master)](https://travis-ci.org/lcamichigan/lease)

This is a collection of resources for creating and distributing leases of the
chapter house of [Sigma Zeta of ΛΧΑ](https://lcamichigan.com).

## Contents

* [Getting Started](#getting-started)
  * [On Windows](#on-windows)
  * [On macOS](#on-macos)
* [How to Make Leases](#how-to-make-leases)
  * [Before Making Leases for the First Time…](#before-making-leases-for-the-first-time)
  * [Update info.json](#update-infojson)
  * [Update tenants.csv](#update-tenantscsv)
  * [Make Leases](#make-leases)
* [Sending Leases](#sending-leases)
* [Example Rent Lists](#example-rent-lists)

## Getting Started

To make leases, you need [LuaTeX](http://www.luatex.org),
[Python](https://www.python.org), and the [Requests](http://python-requests.org)
Python package. All of these are free and cross-platform. You also need the
OpenType version of the font [Linux Libertine](http://libertine-fonts.org). This
is also free, and you’ll get it automatically when you install LuaTeX.

To send leases, you need an email account.

You don’t need to do any TeX or Python programming to make and send leases.
However, you should be familiar with entering commands in PowerShell or Command
Prompt on Windows, or in Terminal on macOS. It’ll also be helpful to have some
exposure to [JSON](https://en.wikipedia.org/wiki/JSON), but this isn’t
essential.

### On Windows

The most reliable way to install LuaTeX is probably to install
[TeX Live](https://www.tug.org/texlive/). To install TeX Live, visit
https://www.tug.org/texlive/acquire-netinstall.html, and then download and run
install-tl-windows.exe. Note that installing TeX Live can take a few hours.

To install Python, visit https://www.python.org/downloads/windows/, and then
download and run an installer for the latest release of Python 2 or 3 (you can
use either version). Make sure you add python.exe to your Windows PATH when you
install Python.

To install the [Requests](http://python-requests.org) package, enter in
PowerShell or Command Prompt:

```batch
pip install requests
```

or, if you don’t have [pip](https://pip.pypa.io/):

```batch
easy_install requests
```

To view leases, you need a PDF viewer. On Windows 10, you can view PDF files in
the built-in
[Microsoft Edge](https://www.microsoft.com/en-us/windows/microsoft-edge)
browser. On Windows 7 and later, you can use
[Adobe Acrobat Reader](https://get.adobe.com/reader/) or
[Google Chrome](https://www.google.com/chrome/).

### On macOS

The easiest way to install LuaTeX is probably to install
[MacTeX](https://www.tug.org/mactex/). To install MacTeX, visit
https://tug.org/mactex/mactex-download.html, download MacTeX.pkg, and then
double-click MacTeX.pkg.

Python is included with macOS.

To install the [Requests](http://python-requests.org) package, enter in Terminal

```sh
sudo easy_install requests
```

## How to Make Leases

First, download this repository as a ZIP archive. To do this, click
[here](https://github.com/lcamichigan/lease/archive/master.zip). Unzip the
archive wherever you wish.

To make leases, you enter commands in PowerShell or Command Prompt on Windows,
or in Terminal on macOS. Open PowerShell or Command Prompt on Windows, or
Terminal on macOS, and then `cd` to the folder you just unzipped.

### Before Making Leases for the First Time…

If you’re making leases for the first time, enter

```sh
python init.py
```

This runs the Python script [init.py](init.py). This script:

1. Downloads a
[disclosure form](https://www.epa.gov/lead/sellers-disclosure-information-lead-based-paint-andor-lead-based-paint-hazards)
and a
[brochure](https://www.epa.gov/lead/protect-your-family-lead-your-home-real-estate-disclosure)
about lead-based paint from the Environmental Protection Agency
2. Creates (at support/SigmaSignature.pdf) a placeholder for the signature that
will be used to sign leases
3. Creates an info.json file and a tenants.csv file

Now, enter

```sh
python make_leases.py
```

This will create (in a folder named “leases”) PDF files of leases using the
information in info.json and tenants.csv. You’ll see placeholder information in
the leases. You must update info.json and tenants.csv with information about the
leases you’re making.

### Update info.json

Open info.json in a text editor (you can use Notepad on Windows or TextEdit on
macOS). The contents of info.json will be something like:

```json
{
    "Name": "Your Name",
    "Title": "Your Title, Sigma Alumni Association",
    "Email address": "your.address@domain.com",

    "Lease description": "Fall 2019 and Winter 2020",
    "Lease due date": "2019-04-01",
    "Lease start date": "2019-08-15",
    "Lease end date": "2020-05-15",
    "Rent": [
        ["2019-08-15", 740],
        ["2019-09-15", 740],
        ["2019-10-15", 740],
        ["2019-11-15", 740],
        ["2019-12-15", 740],
        ["2020-01-15", 740],
        ["2020-02-15", 740],
        ["2020-03-15", 740],
        ["2020-04-15", 740]
    ],
    "Monthly rent during holdover": 1110,

    "Security deposit": 500,
    "Security deposit due date": "2019-05-15",
    "Security deposit location": "ABC Bank, 123 Main St, Anywhere MI 00000-0000",

    "Alumni Advisor name": "John Mason",
    "Alumni Advisor email address": "alumni.advisor@domain.com",
    "Alumni Advisor address": "123 Main St, Elsewhere MI 00000-0000",

    "Sigma signatory name": "Warren Cole",
    "Sigma signatory title": "President"
}
```

Most of info.json is arranged like

```json
"⟨key⟩": "⟨value⟩"
```

You should edit only the values, not the keys. For example, if your name is John
Doe, change

```json
"Name": "Your Name"
```

to

```json
"Name": "John Doe"
```

Dates are formatted as YYYY-MM-DD

The list of monthly rents (starting with `["2019-08", 740]`) assumes a
fall/winter lease with rent at $740/month. See
[Example Rent Lists](#example-rent-lists) for more examples of lists of rent.

### Update tenants.csv

You can open and edit tenants.csv in many applications for working with
spreadsheets, including
[Microsoft Excel](https://products.office.com/en-us/excel),
[Apple Numbers](https://www.apple.com/numbers/), and
[Google Sheets](https://www.google.com/sheets/about/). You can also open
tenants.csv in any text editor.

By default, tenants.csv contains data like this:

Tenant first name | Tenant last name | Email address       | Tenant address | Is Fraternity member | Guarantor name | Guarantor address
------------------|------------------|---------------------|----------------|----------------------|----------------|------------------
Tenant1FirstName  | Tenant1LastName  | address1@domain.com | Tenant1Address | TRUE                 | Guarantor1Name |
Tenant2FirstName  | Tenant2LastName  | address2@domain.com | Tenant2Address | TRUE                 | Guarantor2Name | Guarantor2Address

Replace the default data with information about tenants.

The “Guarantor address” field is optional. If you leave it blank, the guarantor
address will be the same as the tenant address.

### Make Leases

To make leases, enter

```sh
python make_leases.py
```

## Sending Leases

To send leases, enter

```sh
python send_leases.py
```

This script sends to each email address in tenants.csv an email with a lease,
the brochure on lead-based paint you downloaded when you
[ran init.py](#before-making-leases-for-the-first-time), and a move-in form. The
chapter’s alumni advisor will be cc’d on the email.

You’ll be prompted for your email account’s password. If you use a Gmail
account, Gmail will probably reject your log-in attempt. You must “Allow less
secure apps” at https://myaccount.google.com/lesssecureapps to send leases. It’s
a good idea to disallow less secure apps after you send leases.

## Example Rent Lists

Here’s rent for a spring-only lease:

```json
{
    "Lease description": "Spring 2019",
    "Lease due date": "2019-05-01",
    "Lease start date": "2019-05-15",
    "Lease end date": "2019-06-30",
    "Rent": [
        ["2019-05-15", 375]
    ],
    "Monthly rent during holdover": 1110,
}
```

Here’s rent for a spring/summer lease:

```json
{
    "Lease description": "Spring and Summer 2019",
    "Lease due date": "2019-05-01",
    "Lease start date": "2019-05-15",
    "Lease end date": "2019-08-15",
    "Rent": [
        ["2019-05-15", 250],
        ["2019-06-15", 250],
        ["2019-07-15", 250]
    ],
    "Monthly rent during holdover": 1110,
}
```

Here’s rent for a summer-only lease:

```json
{
    "Lease description": "Summer 2019",
    "Lease due date": "2019-05-01",
    "Lease start date": "2019-07-01",
    "Lease end date": "2019-08-15",
    "Rent": [
        ["2019-07-15", 375]
    ],
    "Monthly rent during holdover": 1110,
}
```

Here’s rent for a fall-only lease:

```json
{
    "Lease description": "Fall 2019",
    "Lease due date": "2019-04-01",
    "Lease start date": "2019-08-15",
    "Lease end date": "2019-12-31",
    "Rent": [
        ["2019-08-15", 740],
        ["2019-09-15", 740],
        ["2019-10-15", 740],
        ["2019-11-15", 740],
        ["2019-1-152", 370]
    ],
    "Monthly rent during holdover": 1110,
}
```
