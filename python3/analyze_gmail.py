#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, io
import email
import email.header
import base64
import collections

EMAIL_LABELS = ['from', 'to', 'cc']


class email_stats(object):
    ''' encapsulate email stats '''

    def __init__(self):
        self.email_addresses = collections.defaultdict(int)
        self.number_emails = 0
        self.current_message_stack = []


def parse_quoted_email_string(inpstr):
    if type(inpstr) != str and type(inpstr) != unicode:
        return inpstr

    outstr = inpstr.strip()
    for repl in r'<>()[],':
        outstr = outstr.replace(repl, ' ')
    for repl in r'"\\\'':
        outstr = outstr.replace(repl, '')
    em_list = []
    for word in outstr.split():
        if '@' in word:
            em_list.append(''.join(x[0] for x in email.header.decode_header(word)))
    return em_list


def process_line(line, em_stats_obj=None):
    if not em_stats_obj:
        print('ERROR')
        exit(0)
    try:
        line.find('From ')
    except UnicodeDecodeError:
        print(line.strip())
        print(['%02x' % ord(c) for c in line])
        print('\n'.join(em_stats_obj.current_message_stack))
        exit(0)

    if line.find('From ') == 0:
        if em_stats_obj.current_message_stack:
            msg = email.message_from_string(''.join(em_stats_obj.current_message_stack))
            for k, v in msg.items():
                if k.lower() in EMAIL_LABELS:
                    qstr = ''.join(x[0] for x in email.header.decode_header(v))
                    for estr in parse_quoted_email_string(qstr):
                        em = estr.lower()
                        if '@' not in em:
                            print('bad email?:', em)
                            print(email.header.decode_header(v))
                            exit(0)
                        em_stats_obj.email_addresses[em] += 1
        em_stats_obj.number_emails += 1
        if em_stats_obj.number_emails % 10000 == 0:
            print('N emails:', em_stats_obj.number_emails)
        em_stats_obj.current_message_stack = []
    em_stats_obj.current_message_stack.append(line)


def analyze_gmail(fname):
    em_stats = email_stats()
    with open(fname, 'r', encoding='utf-8') as infile:
        for line in infile:
            process_line(line, em_stats)
    with open('email_addresses.txt', 'w') as f:
        f.write('EmailAddress,Count\n')
        for k, n in sorted(em_stats.email_addresses.items()):
            f.write('%s,%d\n' % (k, n))


if __name__ == '__main__':
    fn = ''
    if len(os.sys.argv) > 1 and os.path.exists(os.sys.argv[1]):
        fn = os.sys.argv[1]
    elif os.path.exists('temp.mbox'):
        fn = 'temp.mbox'
    elif os.path.exists('All mail Including Spam and Trash.mbox'):
        fn = 'All mail Including Spam and Trash.mbox'
    if fn:
        analyze_gmail(fn)
