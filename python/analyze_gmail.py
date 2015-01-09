#!/usr/bin/python

import os
import numpy as np
from dateutil import parser
import email
import email.header
import base64
# from memory_profiler import profile

EMAIL_LABELS = ['from', 'to', 'cc']

def parse_quoted_email_string(inpstr):
    if type(inpstr) != str:
        return inpstr
    
    outstr = inpstr.strip()
    for repl in r'<>()[],':
        outstr = outstr.replace(repl, ' ')
    for repl in r'"\\\'':
        outstr = outstr.replace(repl, '')
    em_list = []
    for word in outstr.split():
        if '@' in word:
            em_list.append(word)
    return em_list

def analyze_gmail(fname):
    email_addresses = {}
    number_emails = 0
    with open(fname, 'r') as infile:
        current_message_stack = []
        for line in infile:
            #if number_emails >= 10000:
                #break
            if line.find('From ') == 0:
                if current_message_stack:
                    msg = email.message_from_string(''.join(current_message_stack))
                    for k, v in msg.items():
                        if k.lower() in EMAIL_LABELS:
                            #print ''.join(x[0] for x in email.header.decode_header(v))
                            #raw_input()
                            for estr in parse_quoted_email_string(''.join(x[0] for x in email.header.decode_header(v))):
                                # print estr
                                em = estr.lower()
                                if '@' not in em:
                                    print 'bad email?:', em
                                    print  email.header.decode_header(v)
                                    exit(0)
                                if em not in email_addresses:
                                    email_addresses[em] = 0
                                email_addresses[em] += 1
                number_emails += 1
                if number_emails % 10000 == 0:
                    print 'N emails:', number_emails
                current_message_stack = []
            current_message_stack.append(line)
    with open('email_addresses.txt', 'w') as f:
        f.write('EmailAddress,Count\n')
        for k, n in sorted(email_addresses.items()):
            f.write('%s,%d\n' % (k, n))

if __name__ == '__main__':
    if os.path.exists('temp.mbox'):
        analyze_gmail('temp.mbox')
    if os.path.exists('All mail Including Spam and Trash.mbox'):
        analyze_gmail('All mail Including Spam and Trash.mbox')
