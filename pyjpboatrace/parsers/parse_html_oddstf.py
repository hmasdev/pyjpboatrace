from bs4 import BeautifulSoup
from pyjpboatrace.utils import str2num


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

    # table
    grid_units = soup.select('div.grid_unit')  # probably 2 units
    win_table = grid_units[0].select('div.table1 > table > tbody > tr')
    placeshow_table = grid_units[1].select('div.table1 > table > tbody > tr')

    # parse
    dic = {
        'win': parse_win(win_table),
        'place_show': parse_place_show(placeshow_table)
    }

    return dic
