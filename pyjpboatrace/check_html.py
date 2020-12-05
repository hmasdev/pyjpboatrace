from bs4 import BeautifulSoup
from .exceptions import NoDataException


def check_html(html: str):

    # whether the dataset has not been displayed
    texts = map(lambda e: e.text, BeautifulSoup(
        html, 'html.parser').select('h3.title12_title'))
    if '※ データはありません。' in texts:
        raise NoDataException()

    # whether the dataset is not found
    texts = map(
        lambda e: e.text,
        BeautifulSoup(html, 'html.parser').select('span.heading1_mainLabel')
    )
    if 'データがありません。' in texts:
        raise NoDataException()
