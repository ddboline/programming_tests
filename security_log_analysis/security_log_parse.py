#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 18:12:50 2015

@author: ddboline
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import shlex
import glob
from subprocess import Popen, PIPE
from dateutil.parser import parse
import datetime
import os, csv, gzip
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from util import dateTimeString

HOSTNAME = os.uname()[1]

MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
               'Oct', 'Nov', 'Dec']

FILE_MAPPING = {'country_code': 'country_code_name.csv.gz',
                'host_country': 'host_country.csv.gz',
                'ssh_log': 'logcsv.csv.gz',
                'apache_log': 'logcsv_apache.csv.gz',
                'ssh_log_cloud': 'logcsv_cloud.csv.gz',
                'apache_log_cloud': 'logcsv_apache_cloud.csv.gz',}

COLUMN_MAPPING = {
'country_code': [{'name': 'Code', 'type': 'char', 'isnull': False},
                 {'name': 'Country', 'type': 'char', 'isnull': False}],
'host_country': [{'name': 'Host', 'type': 'char', 'isnull': False},
                 {'name': 'Code', 'type': 'char', 'isnull': False}],
'ssh_log': [{'name': 'Datetime', 'type': 'datetime', 'isnull': False},
            {'name': 'Host', 'type': 'char', 'isnull': False},
            {'name': 'User', 'type': 'char', 'isnull': False}],
'apache_log': [{'name': 'Datetime', 'type': 'datetime', 'isnull': False},
               {'name': 'Host', 'type': 'char', 'isnull': False},],
'ssh_log_cloud': [{'name': 'Datetime', 'type': 'datetime', 'isnull': False},
            {'name': 'Host', 'type': 'char', 'isnull': False},
            {'name': 'User', 'type': 'char', 'isnull': False}],
'apache_log_cloud': [{'name': 'Datetime', 'type': 'datetime', 'isnull': False},
               {'name': 'Host', 'type': 'char', 'isnull': False},],}

def create_db_engine():
    user = 'ddboline'
    pwd = 'BQGIvkKFZPejrKvX'
    host = 'localhost'
    port = 5432
    dbname = 'ssh_intrusion_logs'
    dbstring = 'postgresql://%s:%s@%s:%s/%s' % (user, pwd, host, port, dbname)
    engine = create_engine(dbstring)
    return engine

def str_len(x):
    try:
        return len(x)
    except:
        return 0

def create_table(df_, table_name='country_code'):
    output = 'CREATE TABLE %s ' % table_name
    vals = []
    for vdict in COLUMN_MAPPING[table_name]:
        cname = vdict['name']
        if (df_[cname].isnull()).sum() > 0:
            vdict['isnull'] = True
        if vdict['type'] == 'char':
            length = df_[cname].apply(str_len).max()
            if cname == 'User':
                out = 'UserName VARCHAR(%s) ' % (length+1,)
            else:
                out = '%s VARCHAR(%s) ' % (cname, length+1)
        elif vdict['type'] == 'datetime':
            out = '%s TIMESTAMP ' % cname
        if not vdict['isnull']:
            out += 'NOT NULL'
        vals.append(out)
    output += '(%s);' % ', '.join(vals)
    return output

def update_table(df_, table_name='country_code'):
    output = 'INSERT INTO %s ' % table_name
    labels = []
    values = []
    for idx, row in df_.iterrows():
        labs = []
        vals = []
        for vdict in COLUMN_MAPPING[table_name]:
            cname = vdict['name']
            ent = row[cname]
            if ent is np.nan:
                if cname == 'User':
                    labs.append('UserName')
                else:
                    labs.append(cname)
                vals.append('NULL')
            elif vdict['type'] == 'datetime':
                labs.append(cname)
                vals.append('TIMESTAMP\'%s\'' % ent)
            elif vdict['type'] == 'char':
                if cname == 'User':
                    labs.append('UserName')
                else:
                    labs.append(cname)
                ent = ent.decode(errors='ignore')
                if type(ent) != int and "'" in ent:
                    ent = ent.replace("'", '')
                if type(ent) != int and '%' in ent:
                    ent = ent.replace('%', '')
                vals.append("'%s'" % ent)            
            else:
                labs.append(cname)
                vals.append('%s' % ent)
        if not labels:
            labels = labs
        values.append('(%s)' % ', '.join(vals))
    output += '(%s) VALUES %s;' % (', '.join(labels), ', '.join(values))
    return output

def dump_postgresql_csv():
    engine = create_db_engine()
    for table, fname in FILE_MAPPING.items():
        print(table, fname)
        columns = [d['name'] for d in COLUMN_MAPPING[table]]
        with gzip.open(fname, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(columns)
            cmd = 'select %s from %s' % (', '.join(columns), table)
            for line in engine.execute(cmd):
                csvwriter.writerow(line)
    return

def dump_csv_to_postgresql(create_tables=False):
    if HOSTNAME != 'dilepton-tower':
        _cmd = 'ssh -N -L localhost:5432:localhost:5432 ddboline@ddbolineathome.mooo.com'
        args = shlex.split(_cmd)
        tunnel_process = Popen(args, shell=False)
        time.sleep(5)
    
    engine = create_db_engine()
    hostlist = []
    for table, fname in FILE_MAPPING.items():
        df_ = pd.read_csv(fname, compression='gzip', na_values=['nan'],
                          keep_default_na=False)
        if create_tables:
            cmd = create_table(df_, table)
            print(cmd)
            engine.execute(cmd)
            cmd = update_table(df_, table)
            engine.execute(cmd)
    if create_tables:
        return
    maxtimestamp = datetime.datetime(year=1970, month=1, day=1)
    table = 'ssh_log'
    if HOSTNAME != 'dilepton-tower':
        table = 'ssh_log_cloud'
    for line in engine.execute('select max(datetime) from %s;' % table):
        maxtimestamp = line[0]
    table = 'apache_log'
    if HOSTNAME != 'dilepton-tower':
        table = 'apache_log_cloud'
    for line in engine.execute('select max(datetime) from %s;' % table):
        if line[0] > maxtimestamp:
            maxtimestamp = line[0]
    for line in engine.execute('select host, code from host_country;'):
        host, code = line
        hostlist.append(host)

    for table in ('ssh_log', 'apache_log'):
        fname = FILE_MAPPING[table]
        df_ = pd.read_csv(fname, compression='gzip', na_values=['nan'],
                          keep_default_na=False)
        df_['Datetime'] = df_['Datetime'].apply(lambda x: parse(x, 
                                                            ignoretz=True))
        cond = df_['Datetime'].dropna() > maxtimestamp
        print(df_[cond].shape)
        if df_[cond].shape[0] == 0:
            continue
        if HOSTNAME != 'dilepton-tower':
            cmd = update_table(df_[cond], table_name='%s_cloud' % table)
        else:
            cmd = update_table(df_[cond], table)
        engine.execute(cmd)

    table = 'host_country'    
    fname = FILE_MAPPING[table]
    df_ = pd.read_csv(fname, compression='gzip')
    notinlist = set(df_['Host']) ^ set(hostlist)
    for host in notinlist:
        cond = df_['Host'] == host
        cmd = update_table(df_[cond], table)
        engine.execute(cmd)
    if HOSTNAME != 'dilepton-tower':
        return tunnel_process
    else:
        return

def analyze_file():
    fname = 'logcsv.csv.gz'
    if HOSTNAME != 'dilepton-tower':
        fname = 'logcsv_cloud.csv.gz'
    with gzip.open(fname, 'w') as logcsv:
        logcsv.write('Datetime,Host,User\n')

        for fname in glob.glob('/var/log/auth.log*'):
            print(fname)
            open_fn = open
            if '.gz' in fname:
                open_fn = gzip.open
            with open_fn(fname, 'r') as logf:
                analyze_single_file_ssh(logf, logcsv)

    fname = 'logcsv_apache.csv.gz'
    if HOSTNAME != 'dilepton-tower':
        fname = 'logcsv_apache_cloud.csv.gz'
    with gzip.open(fname, 'w') as logcsv:
        logcsv.write('Datetime,Host\n')

        for fname in glob.glob('/var/log/apache2/access.log*') + \
                glob.glob('/var/log/apache2/ssl_access.log'):
            print(fname)
            open_fn = open
            if '.gz' in fname:
                open_fn = gzip.open
            with open_fn(fname, 'r') as logf:
                analyze_single_file_apache(logf, logcsv)

def find_originating_country(hostname, country_code_list=None):
    if not hasattr(hostname, 'split'):
        return None
    if '.' not in hostname:
        return None
    if len(hostname.split('.')) < 2:
        return None

    output = []
    result = 'find hostname country: %s ' % hostname
    ents = hostname.split('.')
    if len(ents) > 2 and country_code_list and ents[-1].upper() in \
            country_code_list:
        return ents[-1].upper()
    
    while True:
        pipe = Popen('whois %s' % hostname, shell=True, stdin=PIPE,
                     stdout=PIPE, close_fds=True)
        wfile = pipe.stdout
        output = [l for l in wfile]
        pipe.wait()
        break

    output = ''.join(['%s' % s.decode(errors='ignore') for s in output])

    if 'Your connection limit exceeded. Please slow down and try again later.'\
            in output or 'Timeout' in output:
        time.sleep(10)
        print(hostname)
        return find_originating_country(hostname)

    country = None
    for line in output.split('\n'):
        if 'country' in line or 'Country' in line:
            cn_ = line.split()[-1][-2:].upper()
            if country != cn_:
                if country is not None:
                    print('country? %s %s %s' % (country, cn_, hostname))
                country = cn_
        if 'Brazilian resource' in line:
            country = 'BR'

    if 'whois.nic.ad.jp' in output:
        country = 'JP'

    if 'KOREAN' in output:
        country = 'KR'

    if not country and hostname:
        country = find_originating_country('.'.join(hostname.split('.')[1:]))

    if country:
        result += country
    else:
        raise(TypeError('No Country %s %s' % (result, hostname)))
    print(result)

    return country

def analyze_single_line_ssh(line):
    if 'pam_unix' not in line and 'Invalid user' not in line:
        return None, None, None
    ents = line.split()
    month = MONTH_NAMES.index(ents[0]) + 1
    day = int(ents[1])
    hr_ = int(ents[2][0:2])
    mn_ = int(ents[2][3:5])
    sc_ = int(ents[2][6:8])

    date = datetime.datetime(year=2014, month=month, day=day, hour=hr_,
                             minute=mn_, second=sc_)
    if month <= 5:
        date = datetime.datetime(year=2015, month=month, day=day, hour=hr_,
                                 minute=mn_, second=sc_)

    pname = ents[4].split('[')[0]
    if pname != 'sshd':
        return None, None, None
    if ents[5:7] == ['Invalid', 'user']:
        user = None
        host = ents[-1]
        if len(ents) == 10:
            user = ents[-3]
        return date, host, user

    if 'pam_unix' not in ents[5]:
        return None, None, None

    rhost, user = 2*['']
    for ent in ents[6:]:
        if 'rhost' in ent:
            rhost = ent.replace('rhost=', '')
        elif 'user' in ent:
            user = ent.replace('user=', '')

    return date, rhost, user

def analyze_single_file_ssh(infile, logcsv):
    for line in infile:
        d, h, u = analyze_single_line_ssh(line)
        if h in ['24.44.92.189', '129.49.56.207', '75.72.228.84',
                 'ddbolineathome.mooo.com', 'ool-182c5cbd.dyn.optonline.net',
                 'dboline.physics.sunysb.edu']:
            continue
        if d and h and u:
            logcsv.write('%s,%s,%s\n' % (dateTimeString(d), h, u))

def parse_apache_time_str(timestr):
    day = int(timestr[:2])
    mon = int(MONTH_NAMES.index(timestr[3:6]))+1
    year = int(timestr[7:11])
    hour = int(timestr[12:14])
    minute = int(timestr[15:17])
    second = int(timestr[18:20])
    return datetime.datetime(year=year, month=mon, day=day, hour=hour, minute=minute, second=second)

def analyze_single_file_apache(f, logcsv):
    for line in f:
        try:
            h = line.split()[0]
            t = parse_apache_time_str(line.split()[3].replace('[', ''))
            if h in ['24.44.92.189', '129.49.56.207', '75.72.228.84',
                     'ddbolineathome.mooo.com',
                     'ool-182c5cbd.dyn.optonline.net',
                     'dboline.physics.sunysb.edu']:
                continue
            logcsv.write('%s,%s\n' % (dateTimeString(t), h))
        except:
            continue

def get_country_info():
    fname_ssh = 'logcsv.csv.gz'
    fname_http = 'logcsv_apache.csv.gz'
    if HOSTNAME != 'dilepton-tower':
        fname_ssh = 'logcsv_cloud.csv.gz'
        fname_http = 'logcsv_apache_cloud.csv.gz'
    ssh_df = pd.read_csv(fname_ssh, compression='gzip')
    apache_df = pd.read_csv(fname_http, compression='gzip')
    ccode_df = pd.read_csv('country_code_name.csv.gz', compression='gzip')
    country_list = set(ccode_df['Code'])
    for df in [ssh_df, apache_df]:
        df['Datetime'] = pd.to_datetime(df['Datetime'])

    if not os.path.exists('host_country.csv.gz'):
        with gzip.open('host_country.csv.gz', 'w') as f:
            f.write('Host,Code\n')
    host_country_df = pd.read_csv('host_country.csv.gz', compression='gzip')
    
    with gzip.open('host_country.csv.gz', 'w') as output:
        output.write('Host,Code\n')
        for host in host_country_df['Host'].unique():
            hcond = host_country_df['Host'] == host
            output.write('%s,%s\n' % (host, 
                                      list(host_country_df[hcond]['Code'])[0]))
        for df in [ssh_df, apache_df]:
            for host in df['Host'].unique():
                if host in host_country_df['Host'].unique():
                    continue
                country = find_originating_country(host,
                                                   country_code_list
                                                   =country_list)
                if country:
                    pass
                elif isinstance(host, str) or isinstance(host, unicode):
                    if host[-3] == '.':
                        if host[-2:].upper() in list(ccode_df['Code']):
                            country = host[-2:].upper()
                        elif host[-2:] == 'eu':
                            country = 'FR'
                if country:
                    output.write('%s,%s\n' % (host, country))
                    output.flush()
                else:
                    print(host)

if __name__ == '__main__':
    dump_postgresql_csv()
    analyze_file()
    get_country_info()
    dump_csv_to_postgresql(create_tables=False)