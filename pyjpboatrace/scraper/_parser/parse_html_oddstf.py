from bs4 import BeautifulSoup

from ...exceptions import RaceCancelledException
from ...utils import str2num
from .scrape_odds_update_time import scrape_odds_update_time


def parse_html_oddstf(html: str):

    def parse_win(trs):
        # preparation
        lst_tds = [tr.select('td') for tr in trs]
        # parse
        return {
            ''.join(tds[0].text.split()): str2num(tds[2].text,
                                                  float,
                                                  tds[2].text)
            for tds in lst_tds
        }

    def parse_place_show(trs):
        # preparation
        lst_tds = [tr.select('td') for tr in trs]
        # parse
        return {
            ''.join(tds[0].text.split()): list(map(
                lambda s: str2num(s, float, s),
                tds[2].text.split('-')
            ))
            for tds in lst_tds
        }

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # check cancel
    if '※ 該当レースは中止になりました。' in soup.text:
        raise RaceCancelledException()

    # table
    grid_units = soup.select('div.grid_unit')  # probably 2 units
    win_table = grid_units[0].select('div.table1 > table > tbody > tr')
    placeshow_table = grid_units[1].select('div.table1 > table > tbody > tr')

    # parse
    dic = {
        "update": scrape_odds_update_time(soup),
        'win': parse_win(win_table),
        'place_show': parse_place_show(placeshow_table)
    }

    return dic
