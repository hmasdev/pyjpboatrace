from bs4 import BeautifulSoup
from ..utils import str2num
from ..const import BOATS_GEN


def parse_html_raceresult(html: str):

    def parse_ranks(tbodys):
        # preparation
        lst_tds = list(
            map(lambda tbody: tbody.select('tbody > tr > td'), tbodys))
        return [
            {
                'rank': str2num(tds[0].text, int, tds[0].text),
                'boat':str2num(tds[1].text, int, ''),
                'racerid':str2num(tds[2].select('span')[0].text, int, ''),
                'name':''.join(tds[2].select('span')[1].text.split()),
                'time':''.join(tds[3].text.split())
            }
            for tds in lst_tds
        ]

    def parse_starts(tds):
        # preparation
        dic = {f'course{i}': {} for i in BOATS_GEN}

        # extract
        for i, td in enumerate(tds):
            dic[f'course{i+1}']['boat'] = str2num(
                td.select('span')[0].text, int, '')
            dic[f'course{i+1}']['ST'] = str2num(
                td.select('span')[-1].text.split()[0].replace('F.', '-0.'),
                float,
                ''
            )
        return dic

    def parse_payoff(tbodys):
        # preparation
        dic = {}
        lst_trs = list(map(lambda tbody: tbody.select('tbody > tr'), tbodys))

        # trifecta
        tds = lst_trs[0][0].select('td')

        try:
            dic['trifecta'] = {
                'result': ''.join(
                    tds[1].select_one(
                        'div.numberSet1 > div.numberSet1_row'
                    ).text.split()
                ),
                'payoff': str2num(
                    tds[2].select_one('span')
                        .text
                        .replace('¥', '')
                        .replace(',', ''),
                    int,
                    ''
                ),
                'popularity': str2num(tds[3].text, int, '')
            }
        except:
            dic["trifecta"] = {}
        # trio
        tds = lst_trs[1][0].select('td')
        try:
            dic['trio'] = {
                'result': ''.join(
                    tds[1].select_one(
                        'div.numberSet1 > div.numberSet1_row'
                    ).text.split()
                ),
                'payoff': str2num(
                    tds[2].select_one('span')
                        .text
                        .replace('¥', '')
                        .replace(',', ''),
                    int,
                    ''
                ),
                'popularity': str2num(tds[3].text, int, '')
            }
        except:
            dic["tio"] = []

        # exacta
        tds = lst_trs[2][0].select('td')
        try:
            dic['exacta'] = {
                'result': ''.join(
                    tds[1].select_one(
                        'div.numberSet1 > div.numberSet1_row'
                    ).text.split()
                ),
                'payoff': str2num(
                    tds[2].select_one('span')
                        .text
                        .replace('¥', '')
                        .replace(',', ''),
                    int,
                    ''
                ),
                'popularity': str2num(tds[3].text, int, '')
            }
        except:
            dic['exacta'] = {}

        
        # quinella
        tds = lst_trs[3][0].select('td')

        try:
            dic['quinella'] = {
                'result': ''.join(
                    tds[1].select_one(
                        'div.numberSet1 > div.numberSet1_row'
                    ).text.split()
                ),
                'payoff': str2num(
                    tds[2].select_one('span')
                        .text.replace('¥', '')
                        .replace(',', ''),
                    int,
                    ''
                ),
                'popularity': str2num(tds[3].text, int, '')
            }
        except:
            dic['quinella'] = {}

        # quinella place
        trs = lst_trs[4]
        try:
            dic['quinella_place'] = [
                {
                    'result': ''.join(tr.select('td')[-3].text.split()),
                    'payoff': str2num(
                        tr.select('td')[-2]
                        .text
                        .replace('¥', '')
                        .replace(',', ''),
                        int,
                        ''
                    ),
                    'popularity': str2num(tr.select('td')[-1].text, int, '')
                }
                for tr in trs
            ]
        except:
            dic["quinella_place"] = {}


        dic['quinella_place'] = [
            d for d in dic['quinella_place']
            if any(map(lambda v: v != '', d.values()))
        ]
        # win

        try:
            tds = lst_trs[5][0].select('td')
            dic['win'] = {
                'result': ''.join(
                    tds[1].select_one(
                        'div.numberSet1 > div.numberSet1_row'
                    ).text.split()
                ),
                'payoff': str2num(
                    tds[2].select_one('span')
                        .text
                        .replace('¥', '')
                        .replace(',', ''),
                    int,
                    ''
                ),
                'popularity': str2num(tds[3].text, int, '')
            }
        except:
            dic['win'] = {}


        # place show
        trs = lst_trs[6]

        try:
            dic['place_show'] = [
                {
                    'result': ''.join(tr.select('td')[-3].text.split()),
                    'payoff': str2num(
                        tr.select('td')[-2]
                        .text
                        .replace('¥', '')
                        .replace(',', ''),
                        int, ''
                    ),
                    'popularity': str2num(tr.select('td')[-1].text, int, '')
                }
                for tr in trs
            ]
            dic['place_show'] = [
                d for d in dic['place_show']
                if any(map(lambda v: v != '', d.values()))
            ]
        except:
            dic["place_show"] = {}
        

        return dic

    def parse_weather(divs):
        # direction and temperature
        div = divs[0]
        p = [
            c.replace('is-direction', '')
            for c in div.select_one('p')['class'] if 'is-direction' in c
        ][0]
        direction = str2num(p, int, '')
        span = div.select('div.weather1_bodyUnitLabel > span')[-1]
        tempereture = str2num(''.join(span.text.split())[:-1], float, '')
        # weather
        div = divs[1]
        weather = ''.join(div.select_one(
            'div.weather1_bodyUnitLabel > span').text.split())
        # wind speed
        div = divs[2]
        wind_speed = str2num(
            div.select_one(
                'div.weather1_bodyUnitLabel > span.weather1_bodyUnitLabelData'
            ).text.replace('m', ''),
            int,
            ''
        )
        # wind direction
        div = divs[3]
        p = [
            c.replace('is-wind', '')
            for c in div.select_one('p')['class'] if 'is-wind' in c
        ][0]
        wind_direction = str2num(p, int, '')
        # water temperature
        div = divs[4]
        span = div.select('div.weather1_bodyUnitLabel > span')[-1]
        water_tempereture = str2num(''.join(span.text.split())[:-1], float, '')
        # wave height
        div = divs[5]
        wave_height = str2num(
            div.select_one(
                'div.weather1_bodyUnitLabel > span.weather1_bodyUnitLabelData'
            ).text.replace('cm', ''),
            int,
            ''
        )
        return {
            'direction': direction,
            'temperature': tempereture,
            'weather': weather,
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'water_temperature': water_tempereture,
            'wave_height': wave_height,
        }

    def parse_returns(divs):
        lst = sum(
            map(
                lambda div: list(
                    map(lambda span: span.text, div.select('span'))),
                divs
            ),
            []
        )
        lst = list(map(lambda s: str2num(s, int, ''), lst))
        return [e for e in lst if e]

    def parse_kimarite(td):
        return ''.join(td.text.split())

    def parse_note(tds):
        lst = list(map(lambda td: ''.join(td.text.split()), tds))
        return [e for e in lst if e]

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # table
    grid_units = soup.select(
        'div.grid.is-type2.h-clear > div.grid_unit')  # probably 4 units
    # レース中止の場合
    if len(grid_units) == 0:
        dic = {   
        'result': {},
        'start_information': {},
        'payoff': {},
        'weather_information': {},
        'return': {},
        'kimarite': {},
        'note': {}
        }
        return dic

    ranks_table = grid_units[0].select('div.table1 > table > tbody')
    starts_table = grid_units[1].select('div.table1 > table > tbody > tr > td')
    payoff_table = grid_units[2].select('div.table1 > table > tbody')

    inner_grid_units = grid_units[3].select(
        'div.grid.is-type6.h-clear > div.grid_unit'
    )  # probably 2 units
    weather_table = inner_grid_units[0].select(
        'div.weather1 > div.weather1_body > div.weather1_bodyUnit'
    )

    return_table = inner_grid_units[1].select('div.table1')[0].select(
        'table > tbody > tr > td > div.numberSet1 >div.numberSet1_row'
    )

    kimarite = inner_grid_units[1].select('div.table1')[1]\
                                  .select_one('table > tbody > tr > td')

    note_table = grid_units[3].select('div.table1')[-1]\
                              .select('table > tbody > tr > td')

    # parse
    dic = {
        'result': parse_ranks(ranks_table),
        'start_information': parse_starts(starts_table),
        'payoff': parse_payoff(payoff_table),
        'weather_information': parse_weather(weather_table),
        'return': parse_returns(return_table),
        'kimarite': parse_kimarite(kimarite),
        'note': parse_note(note_table)
    }

    return dic
