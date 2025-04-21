from bs4 import BeautifulSoup

from ...exceptions import RaceCancelledException
from ...utils import str2num
from .scrape_odds_update_time import scrape_odds_update_time


def parse_html_odds3f(html: str):

    def parse_trio(trs):
        # preparation
        lst_tds = [tr.select('td') for tr in trs]
        # extract
        dic = {}
        for tds in lst_tds:

            if 'is-fs14' in tds[0]['class']:
                # change b2
                b2 = str2num(tds[0].text, int, tds[0].text)

                for i, (b3, odds) in enumerate(zip(tds[1::3], tds[2::3])):
                    b1 = i + 1
                    b3 = str2num(b3.text, int, -1)
                    if not (b1 < b2 < b3):
                        break
                    dic[f'{b1}={b2}={b3}'] = str2num(
                        odds.text, float, odds.text)

            else:
                # previous b2
                for i, (b3, odds) in enumerate(zip(tds[::2], tds[1::2])):
                    b1 = i + 1
                    b3 = str2num(b3.text, int, -1)
                    if not (b1 < b2 < b3):
                        break
                    dic[f'{b1}={b2}={b3}'] = str2num(
                        odds.text, float, odds.text)

        return dic

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # check cancel
    if '※ 該当レースは中止になりました。' in soup.text:
        raise RaceCancelledException()

    # table
    tables = soup.select('div.table1')  # probably 2 tables
    trio_table = tables[-1].select('table > tbody > tr')

    # parse
    dic = parse_trio(trio_table)
    dic["update"] = scrape_odds_update_time(soup)

    return dic
