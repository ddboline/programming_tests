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
import glob
from subprocess import Popen, PIPE
from dateutil.parser import parse
import datetime
import os, csv, gzip
import pandas as pd
import numpy as np

#from db_tables import (HostCountry, CountryCode, ApacheLog, ApacheLogCloud,
#                       SSHLog, SSHLogCloud)

from util import (dateTimeString, OpenPostgreSQLsshTunnel, HOSTNAME,
                  create_db_engine)

MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
               'Oct', 'Nov', 'Dec']

FILE_MAPPING = {'country_code': 'country_code_name.csv.gz',
                'host_country': 'host_country.csv.gz',
                'ssh_log': 'logcsv.csv.gz',
                'apache_log': 'logcsv_apache.csv.gz',
                'ssh_log_cloud': 'logcsv_cloud.csv.gz',
                'apache_log_cloud': 'logcsv_apache_cloud.csv.gz',}

COLUMN_MAPPING = {
'country_code': [{'name': 'Code', 'type': 'char', 'isnull': False, 'len': 2},
                 {'name': 'Country', 'type': 'char', 'isnull': False, 'len': 50}],
'host_country': [{'name': 'Host', 'type': 'char', 'isnull': False, 'len': 60},
                 {'name': 'Code', 'type': 'char', 'isnull': False, 'len': 2}],
'ssh_log': [{'name': 'Datetime', 'type': 'datetime', 'isnull': False},
            {'name': 'Host', 'type': 'char', 'isnull': False, 'len': 60},
            {'name': 'User', 'type': 'char', 'isnull': False, 'len': 15}],
'apache_log': [{'name': 'Datetime', 'type': 'datetime', 'isnull': False},
               {'name': 'Host', 'type': 'char', 'isnull': False, 'len': 15},],
'ssh_log_cloud': [{'name': 'Datetime', 'type': 'datetime', 'isnull': False},
            {'name': 'Host', 'type': 'char', 'isnull': False, 'len': 60},
            {'name': 'User', 'type': 'char', 'isnull': False, 'len': 15}],
'apache_log_cloud': [{'name': 'Datetime', 'type': 'datetime', 'isnull': False},
               {'name': 'Host', 'type': 'char', 'isnull': False, 'len': 15},],}

def str_len(st_):
    """ length of string, otherwise 0 """
    try:
        return len(st_)
    except Exception as exc:
        print('Exception %s' % exc)
        raise

def create_table(df_, table_name='country_code'):
    """ SQL to create table """
    output = 'CREATE TABLE %s ' % table_name
    vals = []
    for vdict in COLUMN_MAPPING[table_name]:
        cname = vdict['name']
        if (df_[cname].isnull()).sum() > 0:
            vdict['isnull'] = True
        if vdict['type'] == 'char':
            length = df_[cname].apply(str_len).max()
            if 'len' in vdict:
                length = vdict['len']
            if cname == 'User':
                out = 'UserName VARCHAR(%s) ' % (length,)
            else:
                out = '%s VARCHAR(%s) ' % (cname, length)
        elif vdict['type'] == 'datetime':
            out = '%s TIMESTAMP ' % cname
        if not vdict['isnull']:
            out += 'NOT NULL'
        vals.append(out)
    output += '(%s);' % ', '.join(vals)
    return output

def update_table(df_, table_name='country_code'):
    """ SQL to insert rows into table """
    output = 'INSERT INTO %s ' % table_name
    labels = []
    values = []
    for _, row in df_.iterrows():
        labs = []
        vals = []
        for vdict in COLUMN_MAPPING[table_name]:
            cname = vdict['name']
            ent = row[cname]
            if ent is np.nan:
                if cname == 'User':
                    labs.append('UserName')
                    vals.append("'NoUser'")
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
                if 'len' in vdict and len(ent) > vdict['len']:
                    ent = ent[:vdict['len']]
                vals.append("'%s'" % ent)
            else:
                labs.append(cname)
                vals.append('%s' % ent)
        if not labels:
            labels = labs
        values.append('(%s)' % ', '.join(vals))
    output += '(%s) VALUES %s;' % (', '.join(labels), ', '.join(values))
    return output

def dump_sql_csv():
    """ Dump SQL to CSV """
    engine = create_db_engine()
    for table, fname in FILE_MAPPING.items():
        if any(_ in table for _ in ('ssh_log', 'apache_log')):
            continue
        print(table, fname)
        columns = [d['name'] for d in COLUMN_MAPPING[table]]
        with gzip.open(fname, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(columns)
            cmd = 'select %s from %s' % (', '.join(columns), table)
            for line in engine.execute(cmd):
                csvwriter.writerow(line)
    return

def dump_csv_to_sql(create_tables=False):
    """ Dump csv to SQL """
    engine = create_db_engine()
    hostlist = []
    for table, fname in FILE_MAPPING.items():
        if not os.path.exists(fname):
            continue
        df_ = pd.read_csv(fname, compression='gzip', na_values=['nan'],
                          keep_default_na=False)
        if create_tables:
            cmd = create_table(df_, table)
            engine.execute(cmd)
            cmd = update_table(df_, table)
            engine.execute(cmd)
    if create_tables:
        return

    for line in engine.execute('select host, code from host_country;'):
        host, _ = line
        hostlist.append(host)

    table = 'host_country'
    fname = FILE_MAPPING[table]
    df_ = pd.read_csv(fname, compression='gzip')
    notinlist = set(df_['Host']) ^ set(hostlist)
    for host in notinlist:
        cond = df_['Host'] == host
        if np.sum(cond) > 0:
            cmd = update_table(df_[cond], table)
            engine.execute(cmd)

    for table in 'ssh_log', 'apache_log':
        maxtimestamp = datetime.datetime(year=1970, month=1, day=1)
        if HOSTNAME != 'dilepton-tower':
            table += '_cloud'
        cmd = 'select max(datetime) from %s;' % table
        maxtimestamp = list(engine.execute(cmd))[0][0]
        print(table, maxtimestamp)

        fname = FILE_MAPPING[table]
        df_ = pd.read_csv(fname, compression='gzip', na_values=['nan'],
                          keep_default_na=False)
        df_['Datetime'] = df_['Datetime'].apply(lambda x: parse(x,
                                                            ignoretz=True))
        cond = df_['Datetime'].dropna() > maxtimestamp
        print(df_[cond].shape)
        if df_[cond].shape[0] == 0:
            continue
        cmd = update_table(df_[cond], table)
        engine.execute(cmd)

    from socket import gethostbyname
    hosts_to_remove = []
    for host in ('home.ddboline.net', 'cloud.ddboline.net'):
        hosts_to_remove.extend([host, gethostbyname(host)])

    for host in hosts_to_remove:
        for table in 'ssh_log', 'ssh_log_cloud', 'apache_log', 'apache_log_cloud':
            cmd = "delete from %s where host = '%s'" % (table, host)
            engine.execute(cmd)


def analyze_files():
    """ Analyze log files """
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

def find_originating_country(hostname, country_code_list=None, orig_host=None):
    """ Find country associated with hostname, using whois """
    if not hasattr(hostname, 'split'):
        return None
    if '.' not in hostname:
        return None
    if len(hostname.split('.')) < 2:
        return None
    if not orig_host:
        orig_host = hostname

    output = []
    result = 'find hostname country: %s ' % hostname
    ents = hostname.split('.')
    if len(ents) > 2 and country_code_list and ents[-1].upper() in \
            country_code_list:
        return ents[-1].upper()

    pipe = Popen('whois %s' % hostname, shell=True, stdin=PIPE,
                 stdout=PIPE, close_fds=True)
    wfile = pipe.stdout
    output = [l for l in wfile]
    pipe.wait()

    output = ''.join(['%s' % s.decode(errors='ignore') for s in output])

    if 'Your connection limit exceeded. Please slow down and try again later.'\
            in output or 'Timeout' in output:
        time.sleep(10)
        print(hostname)
        return find_originating_country(hostname,
                                        country_code_list=country_code_list,
                                        orig_host=orig_host)

    country = None
    for line in output.split('\n'):
        if 'country' in line or 'Country' in line:
            cn_ = line.split()[-1]
            if cn_ in country_code_list.values():
                _dict = {v: k for (k, v) in country_code_list.items()}
                return _dict[cn_]
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

    if 'hinet.net' in output:
        country = 'CN'

    if not country and hostname:
        country = find_originating_country('.'.join(hostname.split('.')[1:]),
                                           country_code_list=country_code_list,
                                           orig_host=orig_host)

    if country:
        result += country

    return country

def analyze_single_line_ssh(line):
    """ Analyze single line from ssh log file """
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
    if month <= datetime.datetime.now().month:
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
    """ Analyze single ssh log file """
    for line in infile:
        dt_, hst, usr = analyze_single_line_ssh(line)
        if hst in ['24.44.92.189', '129.49.56.207', '75.72.228.84',
                 'home.ddboline.net', 'ool-182c5cbd.dyn.optonline.net',
                 'dboline.physics.sunysb.edu']:
            continue
        if dt_ and hst and usr:
            logcsv.write('%s,%s,%s\n' % (dateTimeString(dt_), hst, usr))

def parse_apache_time_str(timestr):
    """ Parse apache time string """
    day = int(timestr[:2])
    mon = int(MONTH_NAMES.index(timestr[3:6]))+1
    year = int(timestr[7:11])
    hour = int(timestr[12:14])
    minute = int(timestr[15:17])
    second = int(timestr[18:20])
    return datetime.datetime(year=year, month=mon, day=day, hour=hour,
                             minute=minute, second=second)

def analyze_single_file_apache(infile, logcsv):
    """ Analyze single line of apache log file """
    for line in infile:
        try:
            hst = line.split()[0]
            dt_ = parse_apache_time_str(line.split()[3].replace('[', ''))
            if hst in ['24.44.92.189', '129.49.56.207', '75.72.228.84',
                     'home.ddboline.net',
                     'ool-182c5cbd.dyn.optonline.net',
                     'dboline.physics.sunysb.edu']:
                continue
            logcsv.write('%s,%s\n' % (dateTimeString(dt_), hst))
        except:
            continue

def get_country_info():
    """ find host country for each host in host_country.csv.gz """
    fname_ssh = 'logcsv.csv.gz'
    fname_http = 'logcsv_apache.csv.gz'
    if HOSTNAME != 'dilepton-tower':
        fname_ssh = 'logcsv_cloud.csv.gz'
        fname_http = 'logcsv_apache_cloud.csv.gz'
    ssh_df = pd.read_csv(fname_ssh, compression='gzip')
    apache_df = pd.read_csv(fname_http, compression='gzip')
    ccode_df = pd.read_csv('country_code_name.csv.gz', compression='gzip')
    country_list = dict(zip(ccode_df['Code'], ccode_df['Country']))
    for df_ in [ssh_df, apache_df]:
        df_['Datetime'] = pd.to_datetime(df_['Datetime'])

    if not os.path.exists('host_country.csv.gz'):
        with gzip.open('host_country.csv.gz', 'w') as infile:
            infile.write('Host,Code\n')
    host_country_df = pd.read_csv('host_country.csv.gz', compression='gzip')

    with gzip.open('host_country.csv.gz', 'w') as output:
        output.write('Host,Code\n')
        for host in host_country_df['Host'].unique():
            hcond = host_country_df['Host'] == host
            output.write('%s,%s\n' % (host,
                                      list(host_country_df[hcond]['Code'])[0]))
        for df_ in [ssh_df, apache_df]:
            for host in df_['Host'].unique():
                if host in host_country_df['Host'].unique():
                    continue
                country = find_originating_country(host,
                                                   country_code_list
                                                   =country_list)
                if not country and any(isinstance(host, x)
                                       for x in (str, unicode)):
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
                    output.write('%s,%s\n' % (host, country))
                    output.flush()

def test_find_originating_country():
    ccode_df = pd.read_csv('country_code_name.csv.gz', compression='gzip')
    country_list = dict(zip(ccode_df['Code'], ccode_df['Country']))

    host = 'host-219-235-1-84.iphost.gotonets.com'
    country = find_originating_country(hostname=host,
                                       country_code_list=country_list)
    assert country == 'CN'

if __name__ == '__main__':
    with OpenPostgreSQLsshTunnel():
        dump_sql_csv()
        analyze_files()
        get_country_info()
        dump_csv_to_sql(create_tables=False)
