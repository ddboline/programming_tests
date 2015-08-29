#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 18:52:27 2015

@author: ddboline
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from util import HOSTNAME, OpenPostgreSQLsshTunnel, create_db_engine

def dump_csv(engine, table, title):
    import gzip, csv
    from security_log_parse import COLUMN_MAPPING
    columns = [d['name'] for d in COLUMN_MAPPING[table]]
    with gzip.open('%s.csv.gz' % table, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(columns)
        cmd = 'select %s from %s' % (', '.join(columns), table)
        for line in engine.execute(cmd):
            csvwriter.writerow(line)

def plot_time_access(csvfile, title):
    df = pd.read_csv(csvfile, compression='gzip', parse_dates=['Datetime'])

    if 'Datetime' in df.columns:
        df['Date'] = df['Datetime'].apply(lambda d: d.date())
        df['Hours'] = df['Datetime'].apply(lambda x: (x.hour + x.minute/60.
                                                        + x.second/3600.))
        df['Weekdays'] = df['Datetime'].apply(lambda x: x.weekday())

    print(csvfile, title)
    print(df.head())

    sec = df['Hours'].values
    plt.hist(sec, bins=np.linspace(0, 24, 24),
             histtype='step')
    plt.savefig('%s_hour.png' % title, format='png')
    plt.clf()

    sec = df['Weekdays'].values
    plt.hist(sec, bins=np.linspace(0, 7, 7), histtype='step')
    plt.savefig('%s_weekday.png' % title, format='png')
    plt.clf()

def fill_country_plot(engine):
    table = 'country_count'
    outfname = 'ssh_intrusion_attempts.html'
    if HOSTNAME != 'dilepton-tower':
        table = 'country_count_cloud'
        outfname = 'ssh_intrusion_attempts_cloud.html'

    
    with open(outfname, 'w') as output:
        with open('COUNTRY_TEMPLATE.html', 'r') as inpfile:
            for line in inpfile:
                if 'PUTLISTOFCOUNTRIESANDATTEMPTSHERE' in line:
                    cmd = 'select * from %s;' % table
                    for c, n in engine.execute(cmd):
                        output.write("%10s['%s', %d],\n" % ('', c, n))
                else:
                    output.write(line)
    if os.path.exists('%s/public_html' % os.getenv('HOME')):
        os.system('mv %s %s/public_html/' % (outfname, os.getenv('HOME')))
    return


if __name__ == '__main__':
#    dump_sql_csv()

#    plot_time_access('logcsv.csv.gz', 'ssh_access')
    #plot_time_access('logcsv_cloud.csv.gz', 'ssh_access_cloud')
    #plot_time_access('logcsv_apache.csv.gz', 'apache_access')
    #plot_time_access('logcsv_apache_cloud.csv.gz', 'apache_access_cloud')

    with OpenPostgreSQLsshTunnel():
        engine = create_db_engine()

        table = 'ssh_log'
        if HOSTNAME != 'dilepton-tower':
            table = 'ssh_log_cloud'
            
        #dump_csv(engine, table, 'ssh_access')
        plot_time_access('%s.csv.gz' % table, 'ssh_access')

        print(engine.table_names())
        fill_country_plot(engine)
        columns = ('date', 'local', 'remote')
        cmd = "select %s from local_remote_compare" % (', '.join(columns),)
        import gzip, csv
        with gzip.open('local_remote_compare.csv.gz', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(columns)
            for line in engine.execute(cmd):
                csvwriter.writerow(line)
        df = pd.read_csv('local_remote_compare.csv.gz', compression='gzip')
        print(df.to_string(index=False))
