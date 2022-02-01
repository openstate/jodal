import re

from urllib.parse import urljoin
import datafreeze


def _prefix_tag(ns, tag, start='./'):
    prefixes = {
        'dcterms': 'http://purl.org/dc/terms/',
        'srw': 'http://www.loc.gov/zing/srw/',
        'overheidproduct': 'http://standaarden.overheid.nl/product/terms/',
        'sru': 'http://standaarden.overheid.nl/sru'
    }
    if ns in prefixes:
        return '%s{%s}%s' % (start, prefixes[ns], tag)
    else:
        return '%s%s' % (start, tag)


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
            "title": record.find(_prefix_tag('dcterms', 'title', './/')).text,
            "creator": '%s %s' % (
                record.find(_prefix_tag('sru', 'organisatietype', './/')).text,
                record.find(_prefix_tag('dcterms', 'creator', './/')).text,),
            "url": record.find(_prefix_tag('sru', 'publicatieurl_xhtml', './/')).text,
            'retrieved_at': record.find(_prefix_tag('dcterms', 'modified', './/')).text,
            'modified_at': record.find(_prefix_tag('dcterms', 'modified', './/')).text,
            'published_at': record.find(_prefix_tag('dcterms', 'issued', './/')).text,
            'request_id': record.find(_prefix_tag('dcterms', 'identifier', './/')).text,
            'mime_type': 'application/xhtml'
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
        data['description'] = text_content
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
