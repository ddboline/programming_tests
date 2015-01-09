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
    outstr = []
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
                outchar = '\n'
        elif char == '\n':
            outchar = ''
        #elif char == '<':
            #if not in_quotes:
                #outchar = '|'
        #elif char == '>':
            #if not in_quotes:
                #outchar = ''
        outstr.append(outchar)
    return ''.join(outstr)

def analyze_gmail(fname):
    email_addresses = {}
    number_emails = 0
    with open(fname, 'r') as infile:
        current_message_stack = []
        for line in infile:
            if number_emails >= 100:
                break
            if line.find('From ') == 0:
                if current_message_stack:
                    msg = email.message_from_string(''.join(current_message_stack))
                    for k, v in msg.items():
                        if k.lower() in EMAIL_LABELS:
                            #print email.header.decode_header(v)
                            for ent in parse_quoted_email_string(v).split('\n'):
                                print parse_quoted_email_string(ent)
                                #if '|' in ent:
                                    #name, em = ent.split('|')[:2]
                                    #if '@' not in em:
                                        #print email.header.decode_header(v)
                                    #em = em.lower()
                                    #name = name.replace('"','').replace("'",'').strip()
                                    #if em not in email_addresses:
                                        #email_addresses[em] = []
                                    #if name not in email_addresses[em]:
                                        #email_addresses[em].append(name)
                                #elif len(ent.strip()) > 0:
                                    #em = ent.lower()
                                    #if em not in email_addresses:
                                        #email_addresses[em] = []
                                #else:
                                    #continue
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

if __name__ == '__main__':
    if os.path.exists('temp.mbox'):
        analyze_gmail('temp.mbox')
    if os.path.exists('All mail Including Spam and Trash.mbox'):
        analyze_gmail('All mail Including Spam and Trash.mbox')
