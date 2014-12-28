#!/usr/bin/python

import os
import numpy as np
os.sys.path.append('%s' % os.getenv('HOME'))
from scripts.PollMemory import MemoryConsumption


class mail_message(object):
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.current_field = None
        self.message_elements = {}
        self.message_lines = 0
        self.message_chars = 0
    
    def process_line(self, line):
        first_colon = line.find(': ')
        first_space = line.find(' ')
        if line[0].isupper() and first_colon > 0 and first_space > 0 and first_colon+1 == first_space:
            self.current_field = line[:first_colon]
            if self.current_field not in self.message_elements:
                self.message_elements[self.current_field] = []
            self.message_elements[self.current_field].append( line[first_colon+2:] )
        else:
            if self.current_field in self.message_elements:
                self.message_elements[self.current_field].append( line )

    def print_elements(self):
        for k , v in self.message_elements.iteritems():
            print '%s:' % k
            print ''.join(v)

def analyze_gmail():
    memcheck = MemoryConsumption()
    idx = 0
    nmails = 0
    fields = {}
    labels = {}
    email_addresses = {}
    lines_per_email = []
    chars_per_email = []
    lines_in_email = 0
    chars_in_email = 0
    
    with open( 'All mail Including Spam and Trash.mbox' , 'r' ) as inpfile:
        cur_message = mail_message()
        for line in inpfile:
            
    for line in f.xreadlines():
        if len(line) == 0:
            continue
        else:
            lines_in_email += 1
            chars_in_email += len(line)
        if line[0] == ' ':
            continue
        if line[:5] == 'From ':
            #if cur_message.message_elements:
                #cur_message.print_elements()
                #raw_input()
            #cur_message.reset()
            nmails += 1
            lines_per_email.append( lines_in_email )
            chars_per_email.append( chars_in_email )
            if nmails % 10000 == 0 :
                print 'nmails' , nmails , len(fields), len(labels)
                memcheck.print_memory_consumption()
        #cur_message.process_line( line )
        ent = line.split()
        if len(ent) == 0:
            continue
        if ent[0][-1] == ':':
            val = ent[0].split(':')[0]
            if val not in fields:
                fields[val] = 0
                memcheck.poll()
            if val == 'X-Gmail-Labels':
                for e in ent[1:]:
                    for l in e.split(','):
                        if l not in labels:
                            labels[l] = 0
                        labels[l] += 1
            if val in [ 'To' , 'From' , 'CC' , 'BCC' ] :
                for e in ent[1:]:
                    if r'@' in e:
                        em = e.replace(',','').replace('<','').replace('>','').replace('"','')
                        if em not in email_addresses:
                            email_addresses[em] = 0
                        email_addresses[em] += 1
            fields[val] += 1
        idx+=1
    
    memcheck.print_memory_consumption()
    
    ff = open( 'fields.txt' , 'w' )
    for k in sorted( fields.iterkeys() , key=lambda x : fields[x] ):
        ff.write( '%s %s\n' % ( k , fields[k] ) )
    ff.close()
    
    fl = open( 'labels.txt' , 'w' )
    for k in sorted( labels.iterkeys() , key=lambda x : labels[x] ):
        fl.write( '%s %s\n' % ( k , labels[k] ) )
    fl.close()
    
    fe = open( 'email_addresses.txt' , 'w' )
    for k in sorted( email_addresses.iterkeys() , key=lambda x : email_addresses[x] ):
        fe.write( '%s %s\n' % ( k , email_addresses[k] ) )
    fe.close()
    
    
    print 'Nmails', nmails
    print 'lines_per_email', np.mean( np.array( lines_per_email ) )
    print 'chars_per_email', np.mean( np.array( chars_per_email ) )
    
    f.close()

if __name__ == '__main__':
    analyze_gmail()
