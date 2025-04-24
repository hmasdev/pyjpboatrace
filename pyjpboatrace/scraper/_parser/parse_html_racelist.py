from bs4 import BeautifulSoup

from ...utils import str2num


def parse_html_racelist(html: str):

    def parse_trs(trs):
        # preparation
        lst_tds = [tr.select('td')[::-1] for tr in trs]

        # racer info
        # # extract
        tds = lst_tds[0]
        boat = tds.pop().text
        tds.pop()  # racer figure
        temp = sum(
            map(
                lambda div: ''.join(div.get_text('/').split()).split('/'),
                tds.pop().select('div')
            ),
            []  # initial
        )
        temp = [t for t in temp if t]
        racerid, clss, name, branch, birthplace, age, weight = temp

        F, L, aveST = ''.join(tds.pop().get_text(',').split()).split(',')

        global_win, global_in2nd, global_in3rd \
            = ''.join(tds.pop().get_text(',').split()).split(',')

        local_win, local_in2nd, local_in3rd \
            = ''.join(tds.pop().get_text(',').split()).split(',')

        motor_no, motor_in2nd, motor_in3rd \
            = ''.join(tds.pop().get_text(',').split()).split(',')

        boat_no, boat_in2nd, boat_in3rd \
            = ''.join(tds.pop().get_text(',').split()).split(',')

        # # normalize
        # # # to int
        boat = str2num(boat, int, boat)
        racerid = str2num(racerid, int, racerid)
        age = str2num(age[:-1], int, age)
        F = str2num(F[-1], int, F)
        L = str2num(L[-1], int, L)
        motor_no = str2num(motor_no, int, motor_no)
        boat_no = str2num(boat_no, int, boat_no)
        # # # to float
        weight = str2num(weight[:-2], float, weight[:-2])
        aveST = str2num(aveST, float, aveST)
        global_win = str2num(global_win, float, global_win)
        global_in2nd = str2num(global_in2nd, float, global_in2nd)
        global_in3rd = str2num(global_in3rd, float, global_in3rd)
        local_win = str2num(local_win, float, local_win)
        local_in2nd = str2num(local_in2nd, float, local_in2nd)
        local_in3rd = str2num(local_in3rd, float, local_in3rd)
        motor_in2nd = str2num(motor_in2nd, float, motor_in2nd)
        motor_in3rd = str2num(motor_in3rd, float, motor_in3rd)
        boat_in2nd = str2num(boat_in2nd, float, boat_in2nd)
        boat_in3rd = str2num(boat_in3rd, float, boat_in3rd)

        # drop separation
        tds.pop()

        # racer result
        races = []
        boats = []
        courses = []
        STs = []
        ranks = []

        for _ in range(14):  # TODO move 14 to another file.
            # extract
            temp = tds.pop()
            b = ''
            if temp['class'] and ('is-boatColor' in temp['class'][-1]):
                b = int(temp['class'][-1][-1])
            r = int(temp.text) if temp.text.isdigit() else ''
            c = lst_tds[1].pop().text
            c = int(c) if c.isdigit() else ''
            st = str2num(lst_tds[2].pop().text, float, '')
            rnk = lst_tds[3].pop().select_one('a').text
            rnk = int(rnk) if rnk.isdigit() else rnk
            # keep
            races.append(r)
            boats.append(b)
            courses.append(c)
            STs.append(st)
            ranks.append(rnk)

        # to dict
        dic = {
            'racerid': racerid,
            'class': clss,
            'name': name,
            'branch': branch,
            'birthplace': birthplace,
            'age': age,
            'weight': weight,
            'F': F,
            'L': L,
            'aveST': aveST,
            'global_win_pt': global_win,
            'global_in2nd': global_in2nd,
            'global_in3rd': global_in3rd,
            'local_win_pt': local_win,
            'local_in2nd': local_in2nd,
            'local_in3rd': local_in3rd,
            'motor': motor_no,
            'motor_in2nd': motor_in2nd,
            'motor_in3rd': motor_in3rd,
            'boat': boat_no,
            'boat_in2nd': boat_in2nd,
            'boat_in3rd': boat_in3rd,
            'result': [
                dict()
                if all([
                    r == '', b == '', c == '', st == '', rnk == ''
                ]) else
                {
                    'race': r,
                    'boat': b,
                    'course': c,
                    'ST': st,
                    'rank': rnk
                }
                for r, b, c, st, rnk in zip(races, boats, courses, STs, ranks)
            ]
        }

        return f'boat{boat}', dic

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # table
    table = soup.select('div.table1.is-tableFixed__3rdadd > table > tbody')

    # parse
    dic = dict([
        parse_trs(tbody.select('tr'))
        for tbody in table
    ])
    dic['race_title'] = list(map(
        lambda s: ''.join(s.split()),
        soup.select_one('h3').text.split()  # type: ignore
    ))

    return dic
