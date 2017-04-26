#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import numpy as np
from dateutil import parser

labels = {}
email_labels = ['CC', 'From', 'To']
gmail_labels = {}
email_addresses = {}


def parse_header(lines):
    header_entries = {}
    current_label = None
    for line in lines:
        ents = line.split()
        if not ents:
            continue
        if ents[0][-1] == ':' and ents[0][0].isupper():
            label = ents[0][:-1]
            header_entries[label] = [' '.join(ents[1:])]
            current_label = label
            if label not in labels:
                labels[label] = 0
            labels[label] += 1
        elif current_label:
            header_entries[current_label].append(line)
    if 'X-Gmail-Labels' in header_entries:
        for l in header_entries['X-Gmail-Labels'][0].split(','):
            if l not in gmail_labels:
                gmail_labels[l] = 0
            gmail_labels[l] += 1
    #if 'Cc' in header_entries:
    #print header_entries['Cc']
    for lab in header_entries:
        if lab in email_labels:
            for ent in (' '.join(header_entries[lab])).split():
                if any(a not in ent for a in '<>@'):
                    continue
                em = ent.split('<')[1].split('>')[0]
                for char in ["'", '"', '\\']:
                    em = em.replace(char, '')
                if '=' in em:
                    continue
                if '@' not in em:
                    continue
                if em not in email_addresses:
                    email_addresses[em] = 0
                email_addresses[em] += 1


def parse_email(lines):
    header_lines = []
    body_lines = {}
    for line in lines:
        if body_lines:
            for b in body_lines.keys():
                if '%s--' % b in line:
                    bl = body_lines.pop(b)
                    #print 'body:', b, ' '.join(['%s' % len(l) for l in bl])
                elif b in line:
                    body_lines[b].append([])
                elif body_lines[b]:
                    body_lines[b][-1].append(line)
        else:
            header_lines.append(line)

        if 'boundary=' in line:
            b = line.split('boundary=')[-1].replace('"', '')
            body_lines[b] = []

    #print 'header:',len(header_lines)
    parse_header(header_lines)


def parse_mbox(fname):
    ''' parse mbox file '''
    email_lines = None
    number_of_emails = 0
    with open(fname, 'r') as mboxf:
        for line in mboxf:
            if line.find('From ') == 0:
                if email_lines:
                    parse_email(email_lines)
                    number_of_emails += 1
                    #if number_of_emails > 100000:
                #break
                email_lines = []
            email_lines.append(line.replace('\r\n', '').replace('\n', ''))
        if email_lines:
            parse_email(email_lines)
            number_of_emails += 1

    with open('labels.txt', 'w') as loutf:
        loutf.write('%s\n' % '\n'.join('%s %d' % (k, i) for k, i in sorted(labels.items())))
    with open('gmail_labels.txt', 'w') as gloutf:
        gloutf.write('%s\n' % '\n'.join('%s %d' % (k, i) for k, i in sorted(gmail_labels.items())))
    with open('email_addresses.txt', 'w') as eaoutf:
        eaoutf.write('%s\n' % '\n'.join('%s %d' % (k, i)
                                        for k, i in sorted(email_addresses.items())))
    print('labels:', len(labels))
    print('gmail_labels:', len(gmail_labels))
    print('email_addresses:', len(email_addresses))
    print('Nemails:', number_of_emails)


if __name__ == '__main__':
    fname = os.sys.argv[1]
    if os.path.exists(fname):
        parse_mbox(fname)
