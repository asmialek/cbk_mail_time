#!/usr/bin/env python
#
# Very basic example of using Python 3 and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# This script is example code from this blog post:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
# This is an updated version of the original -- modified to work with Python 3.4.

import sys
import imaplib
import getpass
import email
import email.header
import datetime
import pandas as pd
import numpy as np


# LOOK HERE
# https://stackoverflow.com/questions/9847213/how-do-i-get-the-day-of-week-given-a-date-in-python


EMAIL_ACCOUNT = "smialekadam@gmail.com"

# Use 'INBOX' to read inbox.  Note that whatever folder is specified,
# after successfully running this script all emails in that folder
# will be marked as read.
EMAIL_FOLDER = "INBOX"


def process_mailbox(M):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    id_list = data[0].split()
    # id_list = id_list[6167:]
    start = 6417
    end = 6620
    id_list = id_list[start:end]
    # print(id_list)

    timetable = []

    for num in id_list:
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(str(msg['Subject'])))
        subject = str(hdr)
        sender = str(msg['From'])
        if sender == 'root <root@bolero.cbk.waw.pl>':
            # print('!!!!!!!!!!!!!')
            # print('Message %s: %s' % (str(num), str(subject)))

            # Now convert to local date-time
            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
                print(str(num.decode()), ": Local Date :", local_date.strftime("%a, %d %b %Y %H:%M:%S"))


            body = msg.get_payload().split('\n')[2:]

            for line in body:
                if 'wy' in line:
                    timetable.append(line)

    print(timetable)
    return timetable


def count_hours(timetable):
    for line in timetable:
        data = line.split(' ')
        data = list(filter(None, data))
        print(data)
        day = data[1][0:2]
        month = data[1][3:5]
        time = data[6]

        # print(day, month, time)

M = imaplib.IMAP4_SSL('imap.gmail.com')

print('Hello!')

try:
    # rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass('Password: '))
    rv, data = M.login(EMAIL_ACCOUNT, 'adam2121pro')
    print('LOGIN SUCCESSFUL!')
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ")
    sys.exit(1)

# print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    # print("Mailboxes:")
    # print(mailboxes)
    pass

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print("Processing mailbox...\n")
    timetable = process_mailbox(M)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

count_hours(timetable)

M.logout()