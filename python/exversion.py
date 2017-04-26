#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import pandas as pd
from util import get_md5


def urlopen(url_):
    """ wrapper around requests.get.text simulating urlopen """
    import requests
    from requests import HTTPError
    try:
        requests.packages.urllib3.disable_warnings()
    except AttributeError:
        pass

    urlout = requests.get(url_)
    if urlout.status_code != 200:
        print('something bad happened %d' % urlout.status_code)
        raise HTTPError
    return urlout.text


def exversion():
    #    url = urlopen('https://exversion.com/api/v1/dataset/CM6QX9NZV1S080I' + \
    #                  '?key=dc45cc4429&_limit=20')
    url = urlopen('https://www.exversion.com/api/v1/dataset/' + \
                  'V8OP87U9CG6YOCZ?key=dc45cc4429&_limit=10')

    output = json.loads(url)

    df = pd.DataFrame(output['body'])
    df.to_csv('temp.csv', index=False, encoding='utf8')


def test_exversion():
    exversion()
    assert get_md5('temp.csv') == '3ace7624530bc31421e4090044a63cc5'


if __name__ == '__main__':
    exversion()
