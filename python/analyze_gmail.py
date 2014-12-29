#!/usr/bin/python

import os
import numpy as np
from dateutil import parser

class mail_analysis(object):
    labels_with_addresses = [ 'To', 'CC', 'BCC', 'From' ]
    
    def __init__(self):
        self.email_addresses = []
        self.text_msg_lengths = []
        self.html_msg_lengths = []
    
    def analyze_message(self, mail_msg):
        if len(mail_msg.msg_body) > 0:
            self.text_msg_lengths.append(len(mail_msg.msg_body[0]))
        if len(mail_msg.msg_body) > 1:
            self.html_msg_lengths.append(len(mail_msg.msg_body[1]))
        for k in mail_msg.msg_parts:
            if k in self.labels_with_addresses:
                for em in mail_msg.msg_parts[k].split(','):
                    emad = em.strip().replace('"','').replace("'",'')
                    if emad not in self.email_addresses:
                        self.email_addresses.append( emad )

class mail_message(object):
    def __init__(self, msg_date=None):
        self.msg_date = msg_date
        self.msg_parts = {}
        self.msg_body = []


def analyze_gmail():
    number_of_emails = 0
    current_mail_message = None
    this_analysis = mail_analysis()
    with open('temp.mbox', 'r') as infile:
        while True:
            try:
                line = next(infile)
            except StopIteration:
                break
            ents = line.split()
            if line.find('From ') == 0:
                if current_mail_message:
                    this_analysis.analyze_message(current_mail_message)
                number_of_emails += 1
                current_mail_message = mail_message(msg_date=parser.parse(' '.join(line.split()[2:])))
                msg_part_label = None
                msg_part_content = []
                body_boundary = None
            elif len(ents) == 0:
                continue
            elif ents[0][-1] == ':' and ents[0][0].isupper():
                if msg_part_label != None:
                    current_mail_message.msg_parts[msg_part_label] = ' '.join(msg_part_content)
                    msg_part_content = []
                msg_part_label = ents[0][:-1]
                msg_part_content.append(' '.join(ents[1:]))
            elif 'boundary' in ents[0]:
                body_boundary = ents[0].split('"')[1]
            elif body_boundary and body_boundary in ents[0]:
                temp_msg_body = []
                while True:
                    try:
                        line = next(infile)
                    except StopIteration:
                        break
                    if '%s--' % body_boundary in line:
                        current_mail_message.msg_body.append('\n'.join(temp_msg_body))
                        break
                    elif body_boundary in line:
                        current_mail_message.msg_body.append('\n'.join(temp_msg_body))
                        temp_msg_body = []
                    else:
                        temp_msg_body.append(line.replace('\r','').replace('\n',''))
            else:
                msg_part_content.append(line.strip())
        this_analysis.analyze_message(current_mail_message)

    # for k, it in sorted(mail_messages[0].msg_parts.items()):
        # print '%s: %s' % (k, it)
    # for msg in mail_messages[0].msg_body:
        # print len(msg.split())
    for ad in sorted(this_analysis.email_addresses):
        print ad
    print 'number_of_emails', number_of_emails

if __name__ == '__main__':
    analyze_gmail()