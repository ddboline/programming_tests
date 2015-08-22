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
from dateutil.parser import parse

from util import HOSTNAME, OpenPostgreSQLsshTunnel, create_db_engine

def plot_time_access(csvfile, title):
    df = pd.read_csv(csvfile, compression='gzip')

    if 'Datetime' in df.columns:
        df['Datetime'] = df['Datetime'].apply(parse)
        df['Date'] = df['Datetime'].apply(lambda d: d.date())

    print(csvfile, title)
    print(df.describe())
    print(df['Host'].head())
    print(sorted(df['Date'].unique()))

    ts = df['Datetime'].tolist()

    sec = np.array([(x.hour + x.minute/60. + x.second/3600.) for x in ts])
    plt.hist(sec, bins=np.linspace(0, 24, 24), histtype='step')
    plt.savefig('%s_hour.png' % title, format='png')
    plt.clf()

    sec = np.array([x.weekday() for x in ts])
    plt.hist(sec, bins=np.linspace(0, 7, 7), histtype='step')
    plt.savefig('%s_weekday.png' % title, format='png')
    plt.clf()

def fill_country_plot():
    fname_ssh = 'logcsv.csv.gz'
    fname_http = 'logcsv_apache.csv.gz'
    outfname = 'ssh_intrusion_attempts.html'
    if HOSTNAME != 'dilepton-tower':
        fname_ssh = 'logcsv_cloud.csv.gz'
        fname_http = 'logcsv_apache_cloud.csv.gz'
        outfname = 'ssh_intrusion_attempts_cloud.html'
    ssh_df = pd.read_csv(fname_ssh, compression='gzip')
    apache_df = pd.read_csv(fname_http, compression='gzip')
    ccode_df = pd.read_csv('country_code_name.csv.gz', compression='gzip')
    host_country_df = pd.read_csv('host_country.csv.gz', compression='gzip')

    print([x.columns for x in (ssh_df, ccode_df, host_country_df)])
    print([x.shape for x in (ssh_df, ccode_df, host_country_df)])

    ssh_country_df = pd.concat([ssh_df, apache_df])
    ssh_country_df = pd.merge(ssh_country_df, host_country_df, on='Host')
    ssh_country_df = pd.merge(ssh_country_df, ccode_df, on='Code')

    uniq_host_counts = ssh_country_df['Country'].unique()
    uniq_country_counts = ssh_country_df['Country'].value_counts()

    print(uniq_host_counts)
    print(uniq_country_counts)

    with open(outfname, 'w') as output:
        with open('COUNTRY_TEMPLATE.html', 'r') as inpfile:
            for line in inpfile:
                if 'PUTLISTOFCOUNTRIESANDATTEMPTSHERE' in line:
                    for c, n in uniq_country_counts.to_dict().items():
                        output.write("%10s['%s', %d],\n" % ('', c, n))
                else:
                    output.write(line)
    if os.path.exists('%s/public_html' % os.getenv('HOME')):
        os.system('mv %s %s/public_html/' % (outfname, os.getenv('HOME')))
    return


if __name__ == '__main__':
#    dump_sql_csv()

    plot_time_access('logcsv.csv.gz', 'ssh_access')
    #plot_time_access('logcsv_cloud.csv.gz', 'ssh_access_cloud')
    #plot_time_access('logcsv_apache.csv.gz', 'apache_access')
    #plot_time_access('logcsv_apache_cloud.csv.gz', 'apache_access_cloud')

    fill_country_plot()

    with OpenPostgreSQLsshTunnel():
        engine = create_db_engine()
        cmd = "select * from local_remote_compare"
        for line in engine.execute(cmd):
            print(line)