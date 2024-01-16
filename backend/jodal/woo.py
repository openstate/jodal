import re
from urllib.parse import urljoin

import requests
from lxml import etree

WOO_URL = 'https://doi.wooverheid.nl/?doi=nl&dim=publisher&category=Gemeente'

def test():
    print("Test")

def run():
    resp = requests.get(WOO_URL)
    print(resp)
    if resp.status_code != 200:
        return

    html = etree.HTML(resp.content)

    for r in html.xpath("//table//tr"):
        #print(r)
        try:
            l = r.xpath('./td[1]/a/@href')[0]
        except LookupError as e:
            l = None
        gl = urljoin(WOO_URL, l)
        gm = u''.join(r.xpath('./td[1]//text()')).strip()
        name = u''.join(r.xpath('./td[2]//text()'))
        count = u''.join(r.xpath('./td[3]//text()')).replace(',', '')
        if not count:
            count = '0'
        print({'url': gl, 'code': gm, 'name': name, 'count': int(count)})
