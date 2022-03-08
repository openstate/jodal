import re
import datetime

from urllib.parse import urljoin
import datafreeze


def _prefix_tag(ns, tag, start='./'):
    prefixes = {
        'dcterms': 'http://purl.org/dc/terms/',
        'srw': 'http://www.loc.gov/zing/srw/',
        'overheidproduct': 'http://standaarden.overheid.nl/product/terms/',
        'sru': 'http://standaarden.overheid.nl/sru',
        'overheidrg': 'http://standaarden.overheid.nl/cvdr/terms/'
    }
    if ns in prefixes:
        return '%s{%s}%s' % (start, prefixes[ns], tag)
    else:
        return '%s%s' % (start, tag)

def crawl_first(context, data):
    # https://zoekdienst.overheid.nl/sru/Search?version=1.2&operation=searchRetrieve&x-connection=cvdr&startRecord=1&maximumRecords=10&que|lessdified
    yesterday =  datetime.datetime.now().date()
    from_date = context.params.get('from', yesterday)
    context.log.info('Crawling from: %s' % (from_date.isoformat(),))
    url = (
        'https://zoekdienst.overheid.nl/sru/Search?version=1.2&operation='
        'searchRetrieve&x-connection=cvdr&startRecord=1&maximumRecords=10&'
        'query=modified>=%s') % (from_date.isoformat(),)
    context.emit(data={"url": url})

def crawl_simple(context, data):
    # This stage comes after 'fetch' so the 'data' input contains an
    # HTTPResponse object.
    response = context.http.rehash(data)
    url = response.url
    page = response.xml
    total_elem = page.find(_prefix_tag('srw', 'numberOfRecords'))

    paging = context.params.get("paging")
    if not paging:
        context.log.info("Paging disabled")
    else:
        next_page = page.find(_prefix_tag('srw', 'nextRecordPosition'))
        if next_page is not None:
            next_count = int(next_page.text)
            matches = re.search('&startRecord=(\d+)', url)
            if matches is not None:
                current_count = int(matches.group(1))
                next_url = url.replace(
                    '&startRecord='+str(current_count),
                    '&startRecord='+str(next_count))
                context.log.info('Yielding url: %s', next_url)
                context.emit(rule="fetch", data={"url": next_url})

    # Parse the rest of the page to extract structured data.
    context.log.info('Finding records: %s', _prefix_tag('srw', 'record', './/'))
    for record in page.findall(_prefix_tag('srw', 'record', './/')):
        #context.log.info('Found record! %s', record)
        record_data = {
            #"content_hash":
            'id': record.find(_prefix_tag('dcterms', 'identifier', './/')).text,
            "title": record.find(_prefix_tag('dcterms', 'title', './/')).text,
            "author": '%s %s' % (
                record.find(_prefix_tag('sru', 'organisatietype', './/')).text,
                record.find(_prefix_tag('dcterms', 'creator', './/')).text,),
            "url": record.find(_prefix_tag('sru', 'publicatieurl_xhtml', './/')).text,
            'retrieved_at': record.find(_prefix_tag('dcterms', 'modified', './/')).text,
            'modified_at': record.find(_prefix_tag('dcterms', 'modified', './/')).text,
            'published_at': record.find(_prefix_tag('dcterms', 'issued', './/')).text,
            'request_id': record.find(_prefix_tag('dcterms', 'identifier', './/')).text,
            'mime_type': 'text/html',
            'countries': ["nl"],
            'languages': ["nl"],
            'keywords': [r.text for r in record.findall(_prefix_tag('dcterms', 'subject', './/'))],
            'start_date': record.find(_prefix_tag('overheidrg', 'inwerkingtredingDatum', './/')).text,
            'end_date': record.find(_prefix_tag('overheidrg', 'uitwerkingtredingDatum', './/')).text,
            # "author": quote.find('.//small[@class="author"]').text_content(),
            # "tags": ", ".join(
            #     [tag.text_content() for tag in quote.findall('.//a[@class="tag"]')]
            # ),  # noqa
        }
        context.log.info('Parsed result: %s', record_data)
        context.emit(rule="fetch", data=record_data)
        # If 'rule' is not set, it defaults to 'pass', which triggers the
        # final 'store' stage.
        context.emit(data=record_data)
    #context.emit(rule="cleanup", data={"content_hash": response.content_hash})
    context.emit(data=data)

def crawl(context, data):
    # This stage comes after 'fetch' so the 'data' input contains an
    # HTTPResponse object.
    response = context.http.rehash(data)
    url = response.url
    page = response.xml
    total_elem = page.find(_prefix_tag('srw', 'numberOfRecords'))

    context.log.info(total_elem)
    if total_elem is not None:
        total_count = int(total_elem.text)
        matches = re.search('&startRecord=(\d+)', url)
        if matches is not None:
            current_count = int(matches.group(1))
            # if (current_count + 10) < total_count:
            if (current_count + 10) < 30:  # total_count:
                next_url = url.replace(
                    '&startRecord='+str(current_count),
                    '&startRecord='+str(current_count+10))
                context.log.info('Yielding url: %s', next_url)
                context.emit(rule="fetch", data={"url": next_url})
    # Parse the rest of the page to extract structured data.
    context.log.info('Finding records: %s', _prefix_tag('srw', 'record', './/'))
    for record in page.findall(_prefix_tag('srw', 'record', './/')):
        #context.log.info('Found record! %s', record)
        record_data = {
            #"content_hash":
            'id': record.find(_prefix_tag('dcterms', 'identifier', './/')).text,
            "title": record.find(_prefix_tag('dcterms', 'title', './/')).text,
            "author": '%s %s' % (
                record.find(_prefix_tag('sru', 'organisatietype', './/')).text,
                record.find(_prefix_tag('dcterms', 'creator', './/')).text,),
            "url": record.find(_prefix_tag('sru', 'publicatieurl_xhtml', './/')).text,
            'retrieved_at': record.find(_prefix_tag('dcterms', 'modified', './/')).text,
            'modified_at': record.find(_prefix_tag('dcterms', 'modified', './/')).text,
            'published_at': record.find(_prefix_tag('dcterms', 'issued', './/')).text,
            'request_id': record.find(_prefix_tag('dcterms', 'identifier', './/')).text,
            'mime_type': 'text/html',
            'countries': ["nl"],
            'languages': ["nl"],
            'keywords': [r.text for r in record.findall(_prefix_tag('dcterms', 'subject', './/'))]
            # "author": quote.find('.//small[@class="author"]').text_content(),
            # "tags": ", ".join(
            #     [tag.text_content() for tag in quote.findall('.//a[@class="tag"]')]
            # ),  # noqa
        }
        context.log.info('Parsed result: %s', record_data)
        # If 'rule' is not set, it defaults to 'pass', which triggers the
        # final 'store' stage.
        context.emit(data=record_data)
    context.emit(rule="cleanup", data={"content_hash": response.content_hash})


def detail_parse(context, data):
    with context.http.rehash(data) as response:
        url = response.url
        page = response.html
        context.log.info('Getting text content of : %s', url)
        text_content = u''.join(page.xpath('.//text()'))
        data['description'] = re.sub('\s+', ' ', text_content)
        context.log.info(data)
        context.emit(data=data)

def store(context, data):
    # This example uses a database to store structured data, which you can
    # access through context.datastore.
    table = context.datastore[context.params.get("table")]
    # The data is passed in from context.emit of the previous 'crawl' stage.
    table.upsert(data, ["title", "url", "retrieved_at", "modified_at", "published_at", "description"])


def export(context, params):
    table = context.datastore[params["table"]]
    datafreeze.freeze(table, format="json", filename=params["filename"])
