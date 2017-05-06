# Lease

[![Build status](https://ci.appveyor.com/api/projects/status/30r7r9c9uwue29cg?svg=true)](https://ci.appveyor.com/project/lcamichigan/lease)
[![Build Status](https://travis-ci.org/lcamichigan/lease.svg?branch=master)](https://travis-ci.org/lcamichigan/lease)

This is a collection of resources for creating and distributing leases of the
chapter house of [Sigma Zeta of ΛΧΑ](http://lcamichigan.com).

## Getting Started

To make leases, you need [XeTeX](http://xetex.sourceforge.net),
[Python](https://www.python.org), and the [requests](http://python-requests.org)
Python package. All of these are free and cross-platform. You also need the
OpenType version of the font [Linux Libertine](http://www.linuxlibertine.org).
This is also free, and you’ll get it automatically when you install XeTeX.

To send leases, you need an email account, preferably a Gmail account.

You don’t need to do any TeX or Python programming to make and send leases.
However, you should be familiar with entering commands in Command Prompt on
Windows or Terminal on macOS. It’ll also be helpful to have some exposure to
[JSON](https://en.wikipedia.org/wiki/JSON), but this isn’t essential.

### On Windows

The most reliable way to install XeTeX is probably to install
[TeX Live](https://www.tug.org/texlive/). To install TeX Live, visit
https://www.tug.org/texlive/acquire-netinstall.html, and then download and run
install-tl-windows.exe. Note that installing TeX Live can take a few hours.

To install Python, visit https://www.python.org/downloads/windows/, and then
download and run an installer for the latest release of Python 2 or 3 (you can
use either version). Make sure you add python.exe to your Windows PATH when you
install Python.

To install the [requests](http://python-requests.org) package, open a Command
Prompt and enter:

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
[Adobe Acrobat Reader](https://get.adobe.com/reader/).

### On macOS

The easiest way to install XeTeX is probably to install
[MacTeX](http://www.tug.org/mactex/). To install MacTeX, visit
https://tug.org/mactex/mactex-download.html, download MacTeX.pkg, and then
double-click MacTeX.pkg.

After you install MacTeX, you must install the font Linux Libertine system-wide.
One way to do this is to create a symbolic link to the folder containing this
font by entering in Terminal

``` sh
ln -s /usr/local/texlive/2016/texmf-dist/fonts/opentype/public/libertine ~/Library/Fonts/libertine
```

(If you’re using an older version of MacTeX, you’ll need to replace texlive/2016
with, for example, texlive/2015.)

Python is included with macOS.

To install the [requests](http://python-requests.org) package, enter in Terminal

```sh
sudo easy_install requests
```

## How to Make Leases

First, download this repository as a ZIP archive. To do this, click
[here](https://github.com/nwhetsell/lease/archive/master.zip). Unzip the archive
wherever you wish.

To make leases, you enter commands in Command Prompt on Windows or Terminal on
macOS. Open Command Prompt on Windows or Terminal on macOS, and then `cd` to the
folder you just unzipped.

### Before Making Leases for the First Time…

If you’re making leases for the first time,  enter

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

#### info.json

Open info.json in a text editor (you can use Notepad on Windows or TextEdit on
macOS). The contents of info.json will be something like:

```json
{
    "Name": "Your Name",
    "Title": "Your Title, Sigma Alumni Association",
    "Email address": "your.address@gmail.com",
    "SMTP host": "smtp.gmail.com",
    "SMTP port": 587,

    "Lease description": "Fall 2017 and Winter 2018",
    "Lease start date": "2017-08",
    "Lease end date": "2018-05-15",
    "Rent": [
        ["2017-08", 700],
        ["2017-09", 700],
        ["2017-10", 700],
        ["2017-11", 700],
        ["2017-12", 700],
        ["2018-01", 700],
        ["2018-02", 700],
        ["2018-03", 700],
        ["2018-04", 700]
    ],
    "Lease due date": "2017-04-01",

    "Security deposit": 500,
    "Security deposit due date": "2017-05-15",
    "Security deposit location": "ABC Bank, 123 Main St, Anywhere MI 00000-0000",

    "Alumni Advisor name": "John Mason",
    "Alumni Advisor email address": "alumni.advisor@domain.com",
    "Alumni Advisor address": "123 Main St, Elsewhere MI 00000-0000",

    "Sigma signatory name": "Warren Cole",
    "Sigma signatory title": "President",
    "Sigma signature date": "2017-04-27"
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

Keep in mind:

* If you use a Gmail account, you don’t need to change the SMTP host or port
* Dates are formatted as YYYY-MM or YYYY-MM-DD

The list of monthly rents (starting with `["2017-08", 700]`) assumes a
fall/winter lease with rent at $700/month. See
[Example Rent Lists](#example-rent-lists) for more examples of lists of rent.

#### tenants.csv

You can open and edit tenants.csv in many applications for working with
spreadsheets, including
[Microsoft Excel](https://products.office.com/en-us/excel),
[Apple Numbers](https://www.apple.com/numbers/), and
[Google Sheets](https://www.google.com/sheets/about/). You can also open
tenants.csv in any text editor.

By default, tenants.csv contains data like this:

Tenant first name | Tenant last name | Email address       | Tenant address | Guarantor name | Guarantor address
------------------|------------------|---------------------|----------------|----------------|------------------
Tenant1FirstName  | Tenant1LastName  | address1@domain.com | Tenant1Address | Guarantor1Name |
Tenant2FirstName  | Tenant2LastName  | address2@domain.com | Tenant2Address | Guarantor2Name | Guarantor2Address

Replace the default data with information about tenants.

The “Guarantor address” field is optional. If you leave it blank, the guarantor
address will be the same as the tenant address.

### Making Leases

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
the brochure on lead-based paint you downloaded when you ran init.py, and a
move-in form. The chapter’s alumni advisor will be cc’d on the email.

You’ll be prompted for your email account’s password. If you use a Gmail
account, Gmail will probably reject your log-in attempt. You must “Allow less
secure apps” at https://myaccount.google.com/lesssecureapps to send leases. It’s
a good idea to disallow less secure apps after you send leases.

## Example Rent Lists

Here’s a list of summer rent:

```json
{
    "Lease description": "Summer 2018",
    "Lease start date": "2017-05",
    "Lease end date": "2017-08-15",
    "Rent": [
        ["2017-05", 250],
        ["2017-06", 250],
        ["2017-07", 250]
    ],
    "Lease due date": "2017-05-01",
}
```

Here’s rent for a fall-only lease:

```json
{
    "Lease description": "Fall 2017",
    "Lease start date": "2017-08",
    "Lease end date": "2017-12-31",
    "Rent": [
        ["2017-08", 700],
        ["2017-09", 700],
        ["2017-10", 700],
        ["2017-11", 700],
        ["2017-12", 350]
    ],
    "Lease due date": "2017-04-01",
}
```
