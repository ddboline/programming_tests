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
    output = []
    outstr = []
    namestr = ''
    emstr = ''
    in_quotes = False
    for char in inpstr:
        outchar = char
        if char == '"':
            if in_quotes:
                in_quotes = False
            else:
                in_quotes = True
        elif char == ',':
            if not in_quotes:
                outchar = ''
        elif char == '\n':
            outchar = ''
        elif char == '<':
            if not in_quotes:
                namestr = (''.join(outstr)).strip()
                outstr = []
                outchar = ''
        elif char == '>':
            if not in_quotes:
                emstr = (''.join(outstr)).strip()
                output.append( [namestr, emstr] )
                namestr = ''
                emstr = ''
                outstr = []
                outchar = ''
        outstr.append(outchar)
    return output

def analyze_gmail(fname):
    email_addresses = {}
    number_emails = 0
    with open(fname, 'r') as infile:
        current_message_stack = []
        for line in infile:
            #if number_emails >= 10000:
                #break
            if number_emails % 10000 == 0:
                print 'N emails:', number_emails
            if line.find('From ') == 0:
                if current_message_stack:
                    msg = email.message_from_string(''.join(current_message_stack))
                    for k, v in msg.items():
                        if k.lower() in EMAIL_LABELS:
                            for nstr, estr in parse_quoted_email_string(v):
                                em = estr.lower()
                                if '@' not in em:
                                    print 'bad email?:', em
                                nm = email.header.decode_header(nstr)[0][0]
                                nm = nm.replace('"','').replace("'",'').strip()
                                if em not in email_addresses:
                                    email_addresses[em] = []
                                if nm not in email_addresses[em]:
                                    email_addresses[em].append(nm)
                    #if msg.is_multipart():
                        #for p in msg.walk():
                            #if p.get_content_maintype() == 'multipart':
                                #print p.get_filename()
                        #for p in msg.get_payload():
                            #print p.get_content_type()
                            #if p.get_content_type() == 'text/plain':
                                #print p
                            #if p.get_content_type() == 'multipart/alternative':
                                #print p.items()
                            #if p.get_content_type() == 'multipart/related':
                                #print p.items()
                            #if p.get_content_type() == 'image/png':
                                #print p.items()
                                #fn = None
                                #for k, v in p.items():
                                    #if k == 'Content-Type':
                                        #fn = v.split('name=')[1].replace('"','')
                                #print fn
                                #with open(fn, 'w') as f:
                                    #f.write(base64.b64decode(p.get_payload()))                                
                                #print type(p.get_payload())
                    #else:
                        #print msg.get_payload()
                    #raw_input()
                number_emails += 1
                current_message_stack = []
            current_message_stack.append(line)
    #print any('|' in l for l in email_addresses.values())
    with open('email_addresses.txt', 'w') as f:
        for k in sorted(email_addresses):
            f.write('%s\n' % k)
    with open('email_contacts.csv', 'w') as f:
        f.write('Name,Email\n')
        for k in sorted(email_addresses):
            for nm in email_addresses[k]:
                f.write('%s,"%s"\n' % (k, nm))

if __name__ == '__main__':
    if os.path.exists('temp.mbox'):
        analyze_gmail('temp.mbox')
    if os.path.exists('All mail Including Spam and Trash.mbox'):
        analyze_gmail('All mail Including Spam and Trash.mbox')
