import datetime

from bs4 import BeautifulSoup

from ...const import BOATS_GEN


def parse_html_raceindex(html: str):

    def parse_tds(tds):
        # create key and extract date
        temp = tds[0]
        race = temp.select_one('a').text
        d = datetime.datetime.strptime(
            temp.select_one('a')['href'].split('hd=')[-1],
            '%Y%m%d'
        ).strftime('%Y-%m-%d')

        # extract info
        dic = {}
        dic['vote_limit'] = datetime.datetime.strptime(
            ' '.join([d, tds[1].text]),
            '%Y-%m-%d %H:%M'
        ).strftime('%Y-%m-%d %H:%M:%S')
        dic['status'] = ''.join(tds[2].text.split())
        dic['racers'] = {}
        for b in BOATS_GEN:
            divs = tds[2+b].select('div')
            dic['racers'][f'boat{b}'] = {
                'name': divs[0].select_one('a').text.replace("　", ''),
                'class': divs[-1].text
            }
        return race, dic

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # table
    table = soup.select('div.table1 > table > tbody')

    # parse
    dic = dict([
        parse_tds(tbody.select('tr > td'))
        for tbody in table
    ])

    return dic
