#!/usr/bin/python

import os
import numpy as np
from dateutil import parser
import email
# from memory_profiler import profile

def analyze_gmail(fname):
    with open(fname, 'r') as infile:
        current_message_stack = []
        for line in infile:
            if line.find('From ') == 0:
                if current_message_stack:
                    msg = email.message_from_string(''.join(current_message_stack))
                    print msg.items()
                    if msg.is_multipart():
                        for p in msg.get_payload():
                            print p.get_content_type()
                    else:
                        print msg.get_payload()
                    raw_input()
                current_message_stack = []
            current_message_stack.append(line)

if __name__ == '__main__':
    if os.path.exists('temp.mbox'):
        analyze_gmail('temp.mbox')
    if os.path.exists('All mail Including Spam and Trash.mbox'):
        analyze_gmail('All mail Including Spam and Trash.mbox')
