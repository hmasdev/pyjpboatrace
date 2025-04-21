from bs4 import BeautifulSoup

from ...exceptions import RaceCancelledException
from ...utils import str2num
from .scrape_odds_update_time import scrape_odds_update_time


def parse_html_oddsk(html: str):

    def parse_quinellaplace(trs):

        dic = {}
        for i, tr in enumerate(trs):
            tds = tr.select('td')
            b2 = i + 2
            for j, (_, tde) in enumerate(zip(tds[::2], tds[1::2])):
                b1 = j + 1
                if b1 >= b2:  # invalid quinella-place
                    break
                dic[f'{b1}={b2}'] = list(map(
                    lambda s: str2num(s, float, s),
                    tde.text.split('-')
                ))

        return dic

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # check cancel
    if '※ 該当レースは中止になりました。' in soup.text:
        raise RaceCancelledException()

    # table
    tables = soup.select('div.table1')  # probably 2 tables
    quinellaplace_table = tables[-1].select('table > tbody > tr')

    # parse
    dic = parse_quinellaplace(quinellaplace_table)
    dic["update"] = scrape_odds_update_time(soup)

    return dic
