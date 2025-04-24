from bs4 import BeautifulSoup

from ...utils import str2num


def parse_html_beforeinfo(html: str):

    def parse_racers(trs):
        # preparation
        lst_tds = [tr.select('td')[::-1] for tr in trs]
        # extract
        # # 1st tds
        tds = lst_tds[0]
        boat = tds.pop().text
        tds.pop()  # skip racer figure
        name = tds.pop().select_one('a').text
        weight = tds.pop().text
        display_time = tds.pop().text
        tilt = tds.pop().text
        propeller = tds.pop().text
        parts_exchange = list(map(
            lambda li: ''.join(li.text.split()),
            tds.pop().select('ul > li')
        ))
        tds.pop()  # skip heeader-like
        temp = tds.pop()
        r = temp.text
        b = temp['class'][-1][-1] if temp.get("class", "") else ''
        # # 2nd tds
        tds = lst_tds[1]
        c = tds[0].text
        # # 3rd tds
        tds = lst_tds[2]
        st = tds[0].text
        weight_adjustment = tds[2].text
        # # 4th tds
        tds = lst_tds[3]
        rnk = tds[0].select_one('a').text

        # normalize
        name = ''.join(name.split())
        propeller = ''.join(propeller.split())
        # # to int
        boat = str2num(boat, int, boat)
        r = str2num(r, int, '')
        b = str2num(b, int, '')
        c = str2num(c, int, '')
        rnk = str2num(rnk, int, rnk)
        # # to float
        weight = str2num(weight[:-2], float, '')
        weight_adjustment = str2num(weight_adjustment, float, '')
        display_time = str2num(display_time, float, '')
        tilt = str2num(tilt, float, '')
        st = str2num(st, float, '')

        dic = {
            'name': name,
            'weight': weight,
            'weight_adjustment': weight_adjustment,
            'display_time': display_time,
            'tilt': tilt,
            'propeller': propeller,
            'parts_exchange': parts_exchange,
            'previous_race': (
                {}
                if all(map(lambda x: x == '', [r, b, c, rnk, st]))
                else
                {
                    'race': r,
                    'boat': b,
                    'course': c,
                    'ST': st,
                    "rank": rnk
                }
            )
        }

        return f'boat{boat}', dic

    def parse_display(trs):

        dic = {}

        for i, tr in enumerate(trs):
            try:
                spans = tr.select('div > span')
                dic[f'course{i+1}'] = {
                    'boat': str2num(spans[0].text, int, ''),
                    'ST': str2num(
                        spans[2].text.replace('F.', '-0.'),
                        float,
                        ''
                    )
                }
            except IndexError:
                # Case: missing some racers
                dic[f'course{i+1}'] = {
                    'boat': '',
                    'ST': '',
                }

        return dic

    def parse_weather(div):
        # extract
        time = div.select_one('div > p').text.split()[-1]
        divs = div.select('div.weather1 > div.weather1_body > div')
        direction = [
            c
            for c in divs[0].select_one('p')['class']
            if 'is-direction' in c
        ][0]
        temperature = divs[0].select('div > span')[-1].text
        weather = divs[1].select_one('div > span').text
        wind_speed = divs[2].select('div > span')[-1].text
        try:
            wind_direc = [
                c
                for c in divs[3].select_one('p')['class']
                if 'is-wind' in c
            ][0]
        except IndexError:
            wind_direc = ""
        water_temperature = divs[4].select('div > span')[-1].text
        wave_height = divs[5].select('div > span')[-1].text
        # normalize
        direction = str2num(direction.replace('is-direction', ''), int, '')
        temperature = str2num(temperature[:-1], float, '')
        wind_direc = str2num(wind_direc.replace('is-wind', ''), int, '')
        wind_speed = str2num(wind_speed[:-1], float, '')
        water_temperature = str2num(water_temperature[:-1], float, '')
        wave_height = str2num(wave_height[:-2], float, '')
        # to dict
        return {
            'direction': direction,
            'weather': weather,
            'temperature': temperature,
            'wind_direction': wind_direc,
            'wind_speed': wind_speed,
            'water_temperature': water_temperature,
            'wave_height': wave_height,
            'time': time
        }

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # table
    grid_units = soup.select('div.grid_unit')
    table_racer = grid_units[0].select('div.table1 > table > tbody')
    table_display = grid_units[1].select('div.table1 > table > tbody > tr')
    table_weather = grid_units[1].select_one('div.weather1')

    # parse
    dic = dict([
        parse_racers(tbody.select('tr'))
        for tbody in table_racer
    ])
    dic['start_display'] = parse_display(table_display)
    dic['weather_information'] = parse_weather(table_weather)

    return dic
