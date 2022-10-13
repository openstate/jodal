from lxml import etree
import requests

def add_product(title, price, path, api_key, api_secret):
    url = 'https://www.sendowl.com/api/v1/products.xml'
    headers = {"Accept": "application/json"}
    auth = (api_key, api_secret)
    data = {'product[name]':title, 'product[product_type]':'digital', 'product[price]':str(price)}
    files = {'product[attachment]': open(path, 'rb')}
    r = requests.post(url, auth=auth, headers=headers, data=data, files=files)
    xml = etree.XML(r.text)
    return u''.join(xml.xpath('//sales-page-url//text()'))
