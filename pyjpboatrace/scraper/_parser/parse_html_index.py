import datetime

from bs4 import BeautifulSoup

grade_mapper = {
    'is-ippan': 'ippan',
    'is-G3b': 'G3',
    'is-G2b': 'G2',
    'is-G1b': 'G1',
    'is-G3a': 'G3',
    'is-G2a': 'G2',
    'is-G1a': 'G1',
    'is-SGa': "SG",
    'is-lady': 'lady',
    'is-venus': 'venus',
    'is-rookie__3rdadd': 'rookie',
}

timeframe_mapper = {
    'is-morning': 'morning',
    'is_morning': 'morning',
    'is_summer': 'summer',
    'is-summer': 'summer',
    'is_nighter': 'nighter',
    'is-nighter': 'nighter',
    'is_midnight': 'midnight',
    'is-midnight': 'midnight',
}


def parse_html_index(html: str):

    # make table row parser
    def parse_trs(trs):
        # extract tds
        tds = trs[0].select('td')[::-1]

        # extract values
        stadium = tds.pop().select_one('a > img')['alt'].replace('>', '')
        status = tds.pop()

        if not status.has_attr('colspan'):
            # case : there is a race which has not started yet.
            next_race = int(tds.pop().get_text().replace('R', ''))
            next_vote_limit = trs[1].select_one('td').get_text()
            tds.pop()  # ignore vote button

        grade = tds.pop()['class']
        timeframe = tds.pop().get("class", "")
        title = tds.pop().select_one('a').get_text()
        period, day = tds.pop().get_text('\n').split('\n')

        # clean values
        # grade
        grade = list(map(
            lambda s: grade_mapper.get(s, '[FailedToParse]'+s),
            grade
        ))
        # status
        status = status.get_text()
        # time frame
        timeframe = list(map(
            lambda s: timeframe_mapper.get(s, '[FailedToParse]'+s),
            timeframe
        ))
        timeframe = timeframe[0] if timeframe else ''
        # period
        period = period.split('-')

        # to dict
        ldic = {
            'status': status,
            'grade': grade,
            'timeframe': timeframe,
            'title': title,
            'period': period,
            'day': day,
        }

        if 'next_race' in locals():
            ldic['next_race'] = next_race

        if 'next_vote_limit' in locals():
            ldic['next_vote_limit'] = next_vote_limit

        return stadium, ldic

    def normalize_next_vote_limit(ldic):
        if 'next_vote_limit' in ldic:
            temp = ' '.join([d.strftime('%Y-%m-%d'), ldic['next_vote_limit']])
            temp = datetime.datetime.strptime(temp, '%Y-%m-%d %H:%M')
            ldic['next_vote_limit'] = temp.strftime('%Y-%m-%d %H:%M:%S')

    def normalize_period(ldic):
        # to datetime
        ldic['period'] = list(map(
            lambda md: datetime.datetime.strptime(
                '/'.join([str(d.year), md]), '%Y/%m/%d'),
            ldic['period']
        ))
        # validation
        if ldic['period'][0] > ldic['period'][1]:
            ldic['period'][0] = datetime.datetime(
                ldic['period'][0].year-1,
                ldic['period'][0].month,
                ldic['period'][0].day
            )
        ldic['period'] = list(
            map(lambda dt: dt.strftime('%Y-%m-%d'), ldic['period']))

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # extract date
    d = datetime.datetime.strptime(
        soup.select_one('p.btnGroup3_refreshBtn > a')['href'].split('hd=')[-1],  # type: ignore  # noqa
        '%Y%m%d'
    )

    # table
    table = soup.select_one('div.table1').select('table > tbody')  # type: ignore  # noqa

    # parse
    dic = dict([
        parse_trs(tbody.select('tr'))
        for tbody in table
    ])

    # normalize
    for v in dic.values():
        normalize_next_vote_limit(v)
        normalize_period(v)

    return dic
