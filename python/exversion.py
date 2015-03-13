#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import urlopen
import json
import pandas as pd

#url = urlopen('https://exversion.com/api/v1/dataset/CM6QX9NZV1S080I?key=dc45cc4429&_limit=20')
url = urlopen('https://www.exversion.com/api/v1/dataset/V8OP87U9CG6YOCZ?key=dc45cc4429&_limit=10')

output = json.load(url)

df = pd.DataFrame(output['body'])
df.to_csv('temp.csv', index=False, encoding='utf8')
