from datetime import datetime
import locale
import markdown
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_formatted_current_date_dutch():
    return get_formatted_date_dutch(datetime.now())

def get_formatted_current_date_english():
    return get_formatted_date_english(datetime.now())

def get_formatted_date_english(date):
    logger.debug(f"Formatting date EN: {date}")
    
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            # If the string is not in ISO format, you might need to specify the format
            # date = datetime.strptime(date, '%Y-%m-%d')
            return "Invalid date format"
            
    try:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    except locale.Error:
        logger.warning("Failed to set locale to en_US.UTF-8.")

    
    return date.strftime('%A, %d %B %Y')

def get_formatted_current_year():
    return datetime.now().year

def get_formatted_date_dutch(date):
    logger.debug(f"Formatting date NL: {date}")
    
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            # If the string is not in ISO format, you might need to specify the format
            # date = datetime.strptime(date, '%Y-%m-%d')
            return "Invalid date format"
        
    try:
        locale.setlocale(locale.LC_TIME, 'nl_NL.UTF-8')
    except locale.Error:
        logger.warning("Failed to set locale to nl_NL.UTF-8.")

    return date.strftime('%A, %d %B %Y')

def to_markdown(text):
    # Replace single line bullet points with properly formatted ones
    text = re.sub(r':\s*-\s*', ':\n\n- ', text)
    return markdown.markdown(text)

def format_content(content):
    # Remove leading and trailing whitespace
    content = re.sub(r'</?(?!span\b)\w+[^>]*>', '', content)
    content = f'{content} [...]'
    return to_markdown(content)
   
def add_citations_to_text(text, citations):
    if citations is None or len(citations) == 0:
        return text
    
    citations_list = sorted(citations, key=lambda x: x['start'])
    
    text_w_citations = ""
    last_end = 0
    
    for citation in citations_list:
        text_w_citations += text[last_end:citation['start']]
        citation_text = text[citation['start']:citation['end']]
        document_id_list_string = ','.join([f"'{doc_id}'" for doc_id in citation['document_ids']])
        text_w_citations += f'<span class="citation-link" data-document-ids="[{document_id_list_string}]">{citation_text}</span>'
        last_end = citation['end']
    
    text_w_citations += text[last_end:]
    
    return text_w_citations

def format_text(text, citations):
    if citations is None or len(citations) == 0:
        return to_markdown(text)
    
    text_w_citations = add_citations_to_text(text, citations)    
    html_text = to_markdown(text_w_citations)  # Change this line
    return html_text
