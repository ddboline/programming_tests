#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import pandas as pd

def urlopen(url_):
    """ wrapper around requests.get.text simulating urlopen """
    import requests
    from requests import HTTPError
    requests.packages.urllib3.disable_warnings()

    urlout = requests.get(url_)
    if urlout.status_code != 200:
        print('something bad happened %d' % urlout.status_code)
        raise HTTPError
    return urlout.text


#url = urlopen('https://exversion.com/api/v1/dataset/CM6QX9NZV1S080I?key=dc45cc4429&_limit=20')
url = urlopen('https://www.exversion.com/api/v1/dataset/V8OP87U9CG6YOCZ?key=dc45cc4429&_limit=10')

output = json.loads(url)

df = pd.DataFrame(output['body'])
df.to_csv('temp.csv', index=False, encoding='utf8')
