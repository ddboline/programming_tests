#!/usr/bin/python

import os
import numpy as np
from dateutil import parser
# from memory_profiler import profile

def clean_email_address(inp):
    remchars = '<>"\'()[],;'
    for c in remchars:
        inp = inp.replace(c, ' ')
    inp.replace('mailto:','')
    return inp.lower()

class mail_analysis(object):
    labels_with_addresses = ['To', 'CC', 'BCC', 'From']

    def __init__(self):
        self.emails_analyzed = 0
        self.email_addresses = []
        self.text_msg_lengths = []
        self.html_msg_lengths = []

    def analyze_message(self, mail_msg):
        self.emails_analyzed += 1
        if len(mail_msg.msg_body) > 0:
            self.text_msg_lengths.append(len(mail_msg.msg_body[0]))
        if len(mail_msg.msg_body) > 1:
            self.html_msg_lengths.append(len(mail_msg.msg_body[1]))
        if len(mail_msg.msg_body_chars) > 0:
            self.text_msg_lengths.append(mail_msg.msg_body_chars[0])
        if len(mail_msg.msg_body_chars) > 1:
            self.html_msg_lengths.append(mail_msg.msg_body_chars[1])
        for k in mail_msg.msg_parts:
            if k in self.labels_with_addresses:
                for em in clean_email_address(mail_msg.msg_parts[k]).split():
                    if '@' not in em:
                        continue
                    elif em == '@':
                        continue
                    else:
                        if em not in self.email_addresses:
                            self.email_addresses.append(em)

    def print_analysis(self):
        print 'emails', self.emails_analyzed
        print 'addresses', len(self.email_addresses)
        print 'msg_lengths', float(sum(self.text_msg_lengths))/len(self.text_msg_lengths), float(sum(self.html_msg_lengths))/len(self.html_msg_lengths)

class mail_message(object):
    def __init__(self, msg_date=None):
        self.msg_date = msg_date
        self.msg_parts = {}
        self.msg_body_chars = []
        self.msg_body_words = []
        self.msg_body = []

# @profile
def analyze_gmail(fname):
    current_mail_message = None
    this_analysis = mail_analysis()
    body_boundary = None
    with open(fname, 'r') as infile:
        while True:
            #if this_analysis.emails_analyzed > 10000:
            #    break
            try:
                line = next(infile)
            except StopIteration:
                break

            if len(line.strip()) == 0:
                continue

            ents = line.split()
            if len(ents) == 0:
                continue

            if line.find('From ') == 0:
                if current_mail_message:
                    this_analysis.analyze_message(current_mail_message)
                    del current_mail_message
                    if this_analysis.emails_analyzed % 1000 == 0:
                        print this_analysis.emails_analyzed
                current_mail_message = mail_message(msg_date=parser.parse(' '.join(line.split()[2:])))
                msg_part_label = None
                msg_part_content = []
                body_boundary = None
            elif body_boundary != None and body_boundary in ents[0]:
                # temp_msg_body = []
                temp_msg_chars = 0
                temp_msg_words = 0
                while True:
                    try:
                        line = next(infile)
                    except StopIteration:
                        break
                    if line.find('From ') == 0:
                        current_mail_message.msg_body_chars.append(temp_msg_chars)
                        current_mail_message.msg_body_words.append(temp_msg_words)
                        if current_mail_message:
                            this_analysis.analyze_message(current_mail_message)
                            del current_mail_message
                        current_mail_message = mail_message(msg_date=parser.parse(' '.join(line.split()[2:])))
                        msg_part_label = None
                        msg_part_content = []
                        body_boundary = None
                        break
                    elif '%s--' % body_boundary in line:
                        # current_mail_message.msg_body.append('\n'.join(temp_msg_body))
                        current_mail_message.msg_body_chars.append(temp_msg_chars)
                        current_mail_message.msg_body_words.append(temp_msg_words)
                        msg_part_content = []
                        body_boundary = None
                        break
                    elif body_boundary in line:
                        # current_mail_message.msg_body.append('\n'.join(temp_msg_body))
                        # temp_msg_body = []
                        current_mail_message.msg_body_chars.append(temp_msg_chars)
                        current_mail_message.msg_body_words.append(temp_msg_words)
                    else:
                        # temp_msg_body.append(line.replace('\r','').replace('\n',''))
                        temp_msg_chars += len(line.replace('\r','').replace('\n',''))
                        temp_msg_words += len(line.replace('\r','').replace('\n','').split())
                # del temp_msg_body
            elif ents[0][-1] == ':' and ents[0][0].isupper():
                if msg_part_label != None:
                    msg_part_content = ' '.join(msg_part_content)
                    current_mail_message.msg_parts[msg_part_label] = msg_part_content
                    msg_part_content = []
                msg_part_label = ents[0][:-1]
                msg_part_content.append(' '.join(ents[1:]))
            else:
                msg_part_content.append(line.strip())

            if 'boundary=' in line:
                try:
                    body_boundary = line.split()[-1].replace('boundary=3D','').replace('boundary=','').replace('"','').replace(';','')
                except IndexError:
                    print ents[0]
                    exit(0)

        this_analysis.analyze_message(current_mail_message)

    with open('email_addresses.txt', 'w') as outf:
        for ad in sorted(this_analysis.email_addresses):
            outf.write('%s\n' % ad)
    this_analysis.print_analysis()
    print 'number_of_emails', this_analysis.emails_analyzed

if __name__ == '__main__':
    if os.path.exists('temp.mbox'):
        analyze_gmail('temp.mbox')
    if os.path.exists('All mail Including Spam and Trash.mbox'):
        analyze_gmail('All mail Including Spam and Trash.mbox')
