# PyJPBoatRace: Python-based Japanese boatrace tools :speedboat:

![GitHub top language](https://img.shields.io/github/languages/top/hmasdev/pyjpboatrace)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hmasdev/pyjpboatrace?sort=semver)
![GitHub](https://img.shields.io/github/license/hmasdev/pyjpboatrace)
![GitHub last commit](https://img.shields.io/github/last-commit/hmasdev/pyjpboatrace)
[![PyPI version](https://badge.fury.io/py/pyjpboatrace.svg)](https://pypi.org/project/pyjpboatrace/)
![Scheduled Test](https://github.com/hmasdev/pyjpboatrace/actions/workflows/tests_on_schedule.yaml/badge.svg)

Japanese boat race is extremely exciting sports.
It is also fun to predict the results of races.
Prediction like machine learning method requires data.
Thus, this package provides you with useful tools for data analysis and auto-betting for boatrace.

## Installation

### Requirements

If you want to deposit, withdraw and betting with pyjpboatrace,
one of the following browers is required at least:

- Chrome
- Firefox
- Edge

### Dependencies

- python >= 3.9
- requests>=2.28.1
- beautifulsoup4>=4.11.1
- selenium>=4.6

### User installation

```bash
pip install -U pyjpboatrace
```

## How to use

1. (optional) create an instance of UserInformation;
2. (optional) create a selenium driver;
3. create an instance of PyJPBoatrace;
4. execute scraping and operating.

NOTE: you must create a UserInformation instance and a selenium driver to order to deposit, withdraw or bet.

### UserInformation

- `pyjpboatrace.user_information.UserInformation(userid:str, pin:str, auth_pass:str, vote_pass:str, json_file:str)`

NOTE: If you use a json file to create an instance of UserInformation, the json file should contain the following keys: userid, pin, auth_pass and vote_pass.

### Selenium Driver

You can use the following functions to create selenium drivers:

- pyjpboatrace.drivers.create_chrome_driver()
- pyjpboatrace.drivers.create_firefox_driver()
- pyjpboatrace.drivers.create_edge_driver()
- pyjpboatrace.drivers.create_httpget_driver()

NOTE 1: you can use your own selenium driver.

NOTE 2: If you use create_httpget_driver, you cannot execute the following operations, deposit, withdraw or bet.

### Scraping and Operating

PyJPBoatrace provides 2 main functions: scraping and operating.

The former is scraping race information, odds and so on;
the latter is betting, depositing and withdrawing.

#### Scraping

- Get a list of stadiums which hold races on the given day:

  - API:

    - ```python
      PyJPBoatrace().get_stadiums(d: datetime.date) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().Stadiums.get(d: datetime.date) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_stadiums(date(2021, 8, 12)))
    {'date': '2021-08-12',
     'びわこ': {'day': '３日目',
             'grade': ['ippan'],
             'period': ['2021-08-10', '2021-08-15'],
             'status': '-',
             'timeframe': '',
             'title': '滋賀県知事杯争奪第２６回びわこカップ'},
     '三国': {'day': '２日目',
            'grade': ['ippan'],
            'period': ['2021-08-11', '2021-08-16'],
            'status': '-',
            'timeframe': 'morning',
            'title': '第４９回しぶき賞'},
     '下関': {'day': '最終日',
            'grade': ['ippan'],
            'period': ['2021-08-06', '2021-08-12'],
            'status': '-',
            'timeframe': 'nighter',
            'title': 'Ｈａｙａｓｈｉｋａｎｅ杯'},
     '唐津': {'day': '最終日',
            'grade': ['ippan'],
            'period': ['2021-08-07', '2021-08-12'],
            'status': '-',
            'timeframe': 'morning',
            'title': '唐津大賞がばい王者決定戦'},
     '多摩川': {'day': '最終日',
             'grade': ['ippan'],
             'period': ['2021-08-08', '2021-08-12'],
             'status': '-',
             'timeframe': 'summer',
             'title': '第５９回スポーツニッポン賞'},
     '宮島': {'day': '最終日',
            'grade': ['ippan'],
            'period': ['2021-08-07', '2021-08-12'],
            'status': '-',
            'timeframe': '',
            'title': '第５１回スポーツニッポン杯'},
     '尼崎': {'day': '４日目',
            'grade': ['ippan'],
            'period': ['2021-08-09', '2021-08-14'],
            'status': '-',
            'timeframe': '',
            'title': '日本財団会長杯争奪第４９回オール兵庫王座決定戦'},
     '常滑': {'day': '２日目',
            'grade': ['ippan'],
            'period': ['2021-08-11', '2021-08-16'],
            'status': '-',
            'timeframe': '',
            'title': '名鉄杯争奪２０２１納涼お盆レース'},
     '平和島': {'day': '３日目',
             'grade': ['ippan'],
             'period': ['2021-08-10', '2021-08-15'],
             'status': '-',
             'timeframe': 'summer',
             'title': '第６１回デイリースポーツサマーカップ'},
     '戸田': {'day': '初日',
            'grade': ['ippan'],
            'period': ['2021-08-12', '2021-08-17'],
            'status': '-',
            'timeframe': '',
            'title': '第４４回戸田ボート大賞・サンケイスポーツ杯'},
     '桐生': {'day': '３日目',
            'grade': ['ippan'],
            'period': ['2021-08-10', '2021-08-15'],
            'status': '-',
            'timeframe': 'nighter',
            'title': '第５５回報知新聞社杯\u3000お盆レース'},
     '若松': {'day': '４日目',
            'grade': ['ippan'],
            'period': ['2021-08-08', '2021-08-13'],
            'status': '-',
            'timeframe': 'nighter',
            'title': '日刊スポーツ杯お盆特選競走'},
     '蒲郡': {'day': '初日',
            'grade': ['ippan'],
            'period': ['2021-08-12', '2021-08-17'],
            'status': '-',
            'timeframe': 'nighter',
            'title': '日刊スポーツ杯争奪\u3000納涼しぶきお盆特別選抜戦'},
     '鳴門': {'day': '４日目',
            'grade': ['ippan'],
            'period': ['2021-08-09', '2021-08-14'],
            'status': '-',
            'timeframe': 'morning',
            'title': '第５４回渦王杯競走'}}
    ```

    </details>

- To get 12 races held in the given stadium on the given day:

  - API:

    - ```python
      PyJPBoatrace().get_12races(d: datetime.date, stadium: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().Races.get(d: datetime.date, stadium: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_12races(date(2021, 8, 12), 1))
    {'10R': {'racers': {'boat1': {'class': 'B1', 'name': '佐藤航'},
                        'boat2': {'class': 'A1', 'name': '大澤普司'},
                        'boat3': {'class': 'A2', 'name': '橋本久和'},
                        'boat4': {'class': 'A1', 'name': '江口晃生'},
                        'boat5': {'class': 'B1', 'name': '土屋太朗'},
                        'boat6': {'class': 'A2', 'name': '加瀬智宏'}},
             'status': '発売終了',
             'vote_limit': '2021-08-12 19:43:00'},
     '11R': {'racers': {'boat1': {'class': 'A2', 'name': '藤生雄人'},
                        'boat2': {'class': 'A1', 'name': '毒島誠'},
                        'boat3': {'class': 'A2', 'name': '長谷川充'},
                        'boat4': {'class': 'A1', 'name': '上村純一'},
                        'boat5': {'class': 'B1', 'name': '津久井拓也'},
                        'boat6': {'class': 'B1', 'name': '松本純平'}},
             'status': '発売終了',
             'vote_limit': '2021-08-12 20:14:00'},
     '12R': {'racers': {'boat1': {'class': 'A1', 'name': '久田敏之'},
                        'boat2': {'class': 'A1', 'name': '金子拓矢'},
                        'boat3': {'class': 'A2', 'name': '木村浩士'},
                        'boat4': {'class': 'A1', 'name': '椎名豊'},
                        'boat5': {'class': 'A2', 'name': '本橋克洋'},
                        'boat6': {'class': 'A2', 'name': '野村誠'}},
             'status': '発売終了',
             'vote_limit': '2021-08-12 20:45:00'},
     '1R': {'racers': {'boat1': {'class': 'B1', 'name': '渡辺史之'},
                       'boat2': {'class': 'B1', 'name': '島倉都'},
                       'boat3': {'class': 'A2', 'name': '鳥居塚孝博'},
                       'boat4': {'class': 'B1', 'name': '松本純平'},
                       'boat5': {'class': 'A2', 'name': '橋本久和'},
                       'boat6': {'class': 'B2', 'name': '宮崎安奈'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 15:22:00'},
     '2R': {'racers': {'boat1': {'class': 'B1', 'name': '佐口達也'},
                       'boat2': {'class': 'A2', 'name': '本橋克洋'},
                       'boat3': {'class': 'B1', 'name': '寺本昇平'},
                       'boat4': {'class': 'B1', 'name': '津久井拓也'},
                       'boat5': {'class': 'B1', 'name': '久保原秀人'},
                       'boat6': {'class': 'A2', 'name': '中里英夫'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 15:49:00'},
     '3R': {'racers': {'boat1': {'class': 'B1', 'name': '小川時光'},
                       'boat2': {'class': 'A2', 'name': '野村誠'},
                       'boat3': {'class': 'B2', 'name': '黄金井裕子'},
                       'boat4': {'class': 'A2', 'name': '藤生雄人'},
                       'boat5': {'class': 'B1', 'name': '高山秀雄'},
                       'boat6': {'class': 'A1', 'name': '関浩哉'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 16:16:00'},
     '4R': {'racers': {'boat1': {'class': 'B1', 'name': '栗原謙治'},
                       'boat2': {'class': 'A2', 'name': '金子賢志'},
                       'boat3': {'class': 'B1', 'name': '関根彰人'},
                       'boat4': {'class': 'A1', 'name': '金子拓矢'},
                       'boat5': {'class': 'B2', 'name': '大久保佑香'},
                       'boat6': {'class': 'B1', 'name': '土屋太朗'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 16:45:00'},
     '5R': {'racers': {'boat1': {'class': 'B1', 'name': '原加央理'},
                       'boat2': {'class': 'B1', 'name': '佐藤航'},
                       'boat3': {'class': 'B1', 'name': '蜂須瑞生'},
                       'boat4': {'class': 'A2', 'name': '一柳和孝'},
                       'boat5': {'class': 'B1', 'name': '外崎悟'},
                       'boat6': {'class': 'A1', 'name': '毒島誠'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 17:13:00'},
     '6R': {'racers': {'boat1': {'class': 'A1', 'name': '椎名豊'},
                       'boat2': {'class': 'B1', 'name': '久保田美紀'},
                       'boat3': {'class': 'B1', 'name': '太田克哉'},
                       'boat4': {'class': 'B1', 'name': '島倉都'},
                       'boat5': {'class': 'B1', 'name': '金澤一洋'},
                       'boat6': {'class': 'B1', 'name': '寺本昇平'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 17:42:00'},
     '7R': {'racers': {'boat1': {'class': 'A2', 'name': '木村浩士'},
                       'boat2': {'class': 'B1', 'name': '久保原秀人'},
                       'boat3': {'class': 'A1', 'name': '上村純一'},
                       'boat4': {'class': 'B1', 'name': '鹿島敏弘'},
                       'boat5': {'class': 'B2', 'name': '宮崎安奈'},
                       'boat6': {'class': 'B2', 'name': '黄金井裕子'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 18:11:00'},
     '8R': {'racers': {'boat1': {'class': 'A2', 'name': '鳥居塚孝博'},
                       'boat2': {'class': 'B1', 'name': '高山秀雄'},
                       'boat3': {'class': 'B1', 'name': '吉田稔'},
                       'boat4': {'class': 'B1', 'name': '田中定雄'},
                       'boat5': {'class': 'A1', 'name': '久田敏之'},
                       'boat6': {'class': 'B2', 'name': '大久保佑香'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 18:41:00'},
     '9R': {'racers': {'boat1': {'class': 'B1', 'name': '崎利仁'},
                       'boat2': {'class': 'A2', 'name': '中里英夫'},
                       'boat3': {'class': 'B1', 'name': '塚原武之'},
                       'boat4': {'class': 'A1', 'name': '土屋智則'},
                       'boat5': {'class': 'B1', 'name': '関根彰人'},
                       'boat6': {'class': 'A1', 'name': '山崎智也'}},
            'status': '発売終了',
            'vote_limit': '2021-08-12 19:12:00'},
     'date': '2021-08-12',
     'stadium': 1}
    ```

    </details>

- To get the basic information of the race in the stadium on a day:

  - API:

    - ```python
      PyJPBoatrace().get_race_info(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().RaceInfo.get(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_race_info(date(2021, 8, 12), 10, 1))
    {'boat1': {'F': 0,
               'L': 0,
               'age': 47,
               'aveST': 0.16,
               'birthplace': '福井',
               'boat': 13,
               'boat_in2nd': 41.79,
               'boat_in3rd': 58.21,
               'branch': '福井',
               'class': 'A1',
               'global_in2nd': 40.45,
               'global_in3rd': 53.93,
               'global_win_pt': 5.73,
               'local_in2nd': 52.38,
               'local_in3rd': 67.46,
               'local_win_pt': 6.94,
               'motor': 44,
               'motor_in2nd': 53.42,
               'motor_in3rd': 63.01,
               'name': '武田光史',
               'racerid': 3654,
               'result': [{'ST': 0.19,
                           'boat': 5,
                           'course': 5,
                           'race': 6,
                           'rank': 4},
                          {'ST': 0.14,
                           'boat': 3,
                           'course': 3,
                           'race': 12,
                           'rank': 5},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {}],
               'weight': 52.6},
     'boat2': {'F': 0,
               'L': 0,
               'age': 25,
               'aveST': 0.21,
               'birthplace': '愛知',
               'boat': 64,
               'boat_in2nd': 22.67,
               'boat_in3rd': 36.0,
               'branch': '愛知',
               'class': 'B1',
               'global_in2nd': 10.17,
               'global_in3rd': 20.34,
               'global_win_pt': 3.18,
               'local_in2nd': 3.33,
               'local_in3rd': 3.33,
               'local_win_pt': 2.0,
               'motor': 24,
               'motor_in2nd': 42.67,
               'motor_in3rd': 68.0,
               'name': '大澤誠也',
               'racerid': 5074,
               'result': [{'ST': 0.19,
                           'boat': 3,
                           'course': 3,
                           'race': 6,
                           'rank': 3},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {}],
               'weight': 53.1},
     'boat3': {'F': 0,
               'L': 0,
               'age': 45,
               'aveST': 0.17,
               'birthplace': '愛知',
               'boat': 41,
               'boat_in2nd': 29.33,
               'boat_in3rd': 52.0,
               'branch': '愛知',
               'class': 'B1',
               'global_in2nd': 29.79,
               'global_in3rd': 54.26,
               'global_win_pt': 5.39,
               'local_in2nd': 31.48,
               'local_in3rd': 51.85,
               'local_win_pt': 5.09,
               'motor': 51,
               'motor_in2nd': 49.32,
               'motor_in3rd': 63.01,
               'name': '堀本裕也',
               'racerid': 3895,
               'result': [{'ST': 0.06,
                           'boat': 5,
                           'course': 5,
                           'race': 4,
                           'rank': 5},
                          {'ST': 0.2,
                           'boat': 2,
                           'course': 2,
                           'race': 11,
                           'rank': 4},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {}],
               'weight': 50.0},
     'boat4': {'F': 0,
               'L': 0,
               'age': 47,
               'aveST': 0.18,
               'birthplace': '石川',
               'boat': 36,
               'boat_in2nd': 32.43,
               'boat_in3rd': 44.59,
               'branch': '福井',
               'class': 'B1',
               'global_in2nd': 17.17,
               'global_in3rd': 29.29,
               'global_win_pt': 3.99,
               'local_in2nd': 21.59,
               'local_in3rd': 35.23,
               'local_win_pt': 4.45,
               'motor': 41,
               'motor_in2nd': 45.95,
               'motor_in3rd': 64.86,
               'name': '信濃由行',
               'racerid': 3620,
               'result': [{'ST': 0.26,
                           'boat': 5,
                           'course': 3,
                           'race': 3,
                           'rank': 5},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {}],
               'weight': 52.3},
     'boat5': {'F': 0,
               'L': 0,
               'age': 30,
               'aveST': 0.19,
               'birthplace': '石川',
               'boat': 17,
               'boat_in2nd': 21.79,
               'boat_in3rd': 46.15,
               'branch': '福井',
               'class': 'B1',
               'global_in2nd': 37.5,
               'global_in3rd': 56.73,
               'global_win_pt': 5.56,
               'local_in2nd': 35.04,
               'local_in3rd': 52.55,
               'local_win_pt': 5.53,
               'motor': 61,
               'motor_in2nd': 43.28,
               'motor_in3rd': 64.18,
               'name': '木田峰由季',
               'racerid': 4587,
               'result': [{'ST': 0.19,
                           'boat': 2,
                           'course': 2,
                           'race': 3,
                           'rank': 3},
                          {'ST': 0.21,
                           'boat': 4,
                           'course': 5,
                           'race': 10,
                           'rank': 2},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {}],
               'weight': 52.2},
     'boat6': {'F': 0,
               'L': 0,
               'age': 21,
               'aveST': '-',
               'birthplace': '福井',
               'boat': 15,
               'boat_in2nd': 26.76,
               'boat_in3rd': 39.44,
               'branch': '福井',
               'class': 'B2',
               'global_in2nd': 0.0,
               'global_in3rd': 0.0,
               'global_win_pt': 1.29,
               'local_in2nd': 0.0,
               'local_in3rd': 0.0,
               'local_win_pt': 1.0,
               'motor': 54,
               'motor_in2nd': 43.84,
               'motor_in3rd': 63.01,
               'name': '加藤優弥',
               'racerid': 5185,
               'result': [{'ST': 0.01,
                           'boat': 6,
                           'course': 6,
                           'race': 4,
                           'rank': 6},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {}],
               'weight': 52.6},
     'date': '2021-08-12',
     'race': 1,
     'race_title': ['みくにあさイチ', '1800m'],
     'stadium': 10}
    ```

    </details>

- To get the odds of win (単勝) and place-show (複勝) of the race in the stadium on the day:

  - API:

    - ```python
      PyJPBoatrace().get_odds_win_placeshow(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().WinPlaceshowOdds.get(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_odds_win_placeshow(date(2021, 8, 12), 10, 1))
    {'date': '2021-08-12',
     'place_show': {'1': [1.0, 1.0],
                    '2': [2.5, 7.0],
                    '3': [2.0, 5.5],
                    '4': [2.3, 6.4],
                    '5': [1.5, 4.0],
                    '6': [3.8, 10.6]},
     'race': 1,
     'stadium': 10,
     'update': '締切時オッズ',
     'win': {'1': 1.0, '2': 20.7, '3': 11.0, '4': 18.4, '5': 23.6, '6': 27.6}}
    ```

    </details>

- To get the odds of quinella place (拡連複) of the race in the stadioum on the day:

  - API:

    - ```python
      PyJPBoatrace().get_odds_quinellaplace(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().QuinellaplaceOdds.get(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_odds_quinellaplace(date(2021, 8, 12), 10, 1))
    {'1=2': [1.6, 2.1],
     '1=3': [1.1, 1.4],
     '1=4': [3.7, 5.0],
     '1=5': [1.1, 1.4],
     '1=6': [18.1, 23.4],
     '2=3': [6.1, 9.9],
     '2=4': [10.6, 13.0],
     '2=5': [4.1, 6.4],
     '2=6': [30.1, 34.8],
     '3=4': [5.1, 7.1],
     '3=5': [1.9, 3.4],
     '3=6': [16.9, 22.4],
     '4=5': [6.4, 8.9],
     '4=6': [50.0, 51.9],
     '5=6': [16.0, 20.9],
     'date': '2021-08-12',
     'race': 1,
     'stadium': 10,
     'update': '締切時オッズ'}
    ```

    </details>

- To get the odds of exacta (二連単) and quinella (二連複) of the race in the stadioum on the day:

  - API:

    - ```python
      PyJPBoatrace().get_odds_exacta_quinella(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().ExactaQuinellaOdds.get(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_odds_exacta_quinella(date(2021, 8, 12), 10, 1))
    {'date': '2021-08-12',
     'exacta': {'1-2': 4.8,
                '1-3': 2.6,
                '1-4': 7.2,
                '1-5': 4.0,
                '1-6': 63.9,
                '2-1': 26.4,
                '2-3': 75.9,
                '2-4': 291.8,
                '2-5': 132.6,
                '2-6': 810.5,
                '3-1': 15.9,
                '3-2': 94.7,
                '3-4': 110.5,
                '3-5': 41.2,
                '3-6': 429.1,
                '4-1': 66.9,
                '4-2': 260.5,
                '4-3': 187.0,
                '4-5': 105.7,
                '4-6': 455.9,
                '5-1': 13.5,
                '5-2': 74.4,
                '5-3': 47.9,
                '5-4': 70.8,
                '5-6': 97.2,
                '6-1': 347.3,
                '6-2': 663.2,
                '6-3': 729.5,
                '6-4': 729.5,
                '6-5': 455.9},
     'quinella': {'1=2': 4.8,
                  '1=3': 1.8,
                  '1=4': 6.1,
                  '1=5': 4.4,
                  '1=6': 73.8,
                  '2=3': 79.5,
                  '2=4': 94.0,
                  '2=5': 36.9,
                  '2=6': 172.3,
                  '3=4': 64.6,
                  '3=5': 16.6,
                  '3=6': 206.8,
                  '4=5': 33.3,
                  '4=6': 172.3,
                  '5=6': 129.2},
     'race': 1,
     'stadium': 10,
     'update': '締切時オッズ'}
    ```

    </details>

- To get the odds of trifecta (三連単) of the race in the stadioum on the day:

  - API:

    - ```python
      PyJPBoatrace().get_odds_trifecta(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBaotrace().TrifectaOdds.get(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_odds_trifecta(date(2021, 8, 12), 10, 1))
    {'1-2-3': 12.1,
     '1-2-4': 22.8,
     '1-2-5': 10.7,
     '1-2-6': 136.2,
     '1-3-2': 11.2,
     '1-3-4': 9.5,
     '1-3-5': 5.2,
     '1-3-6': 101.2,
     '1-4-2': 33.9,
     '1-4-3': 19.2,
     '1-4-5': 18.8,
     '1-4-6': 169.1,
     '1-5-2': 11.9,
     '1-5-3': 7.3,
     '1-5-4': 16.0,
     '1-5-6': 81.5,
     '1-6-2': 400.4,
     '1-6-3': 357.7,
     '1-6-4': 399.1,
     '1-6-5': 297.0,
     '2-1-3': 143.1,
     '2-1-4': 251.5,
     '2-1-5': 135.8,
     '2-1-6': 759.3,
     '2-3-1': 274.6,
     '2-3-4': 926.4,
     '2-3-5': 574.7,
     '2-3-6': 1866.0,
     '2-4-1': 715.5,
     '2-4-3': 1247.0,
     '2-4-5': 981.4,
     '2-4-6': 2853.0,
     '2-5-1': 256.5,
     '2-5-3': 542.1,
     '2-5-4': 838.8,
     '2-5-6': 1306.0,
     '2-6-1': 2789.0,
     '2-6-3': 3103.0,
     '2-6-4': 4138.0,
     '2-6-5': 2342.0,
     '3-1-2': 81.8,
     '3-1-4': 69.4,
     '3-1-5': 35.9,
     '3-1-6': 403.0,
     '3-2-1': 238.0,
     '3-2-4': 709.4,
     '3-2-5': 432.5,
     '3-2-6': 1469.0,
     '3-4-1': 206.0,
     '3-4-2': 684.0,
     '3-4-5': 226.7,
     '3-4-6': 1591.0,
     '3-5-1': 82.6,
     '3-5-2': 282.4,
     '3-5-4': 221.2,
     '3-5-6': 775.9,
     '3-6-1': 1970.0,
     '3-6-2': 2364.0,
     '3-6-4': 3027.0,
     '3-6-5': 2387.0,
     '4-1-2': 330.1,
     '4-1-3': 207.7,
     '4-1-5': 179.9,
     '4-1-6': 989.2,
     '4-2-1': 780.8,
     '4-2-3': 1452.0,
     '4-2-5': 977.5,
     '4-2-6': 2789.0,
     '4-3-1': 477.4,
     '4-3-2': 1286.0,
     '4-3-5': 556.7,
     '4-3-6': 2586.0,
     '4-5-1': 259.4,
     '4-5-2': 598.3,
     '4-5-3': 399.1,
     '4-5-6': 1030.0,
     '4-6-1': 2728.0,
     '4-6-2': 3310.0,
     '4-6-3': 3762.0,
     '4-6-5': 3267.0,
     '5-1-2': 67.2,
     '5-1-3': 46.4,
     '5-1-4': 103.0,
     '5-1-6': 287.0,
     '5-2-1': 197.0,
     '5-2-3': 420.8,
     '5-2-4': 656.8,
     '5-2-6': 1205.0,
     '5-3-1': 100.8,
     '5-3-2': 324.9,
     '5-3-4': 332.8,
     '5-3-6': 1149.0,
     '5-4-1': 258.3,
     '5-4-2': 625.4,
     '5-4-3': 414.5,
     '5-4-6': 1286.0,
     '5-6-1': 800.9,
     '5-6-2': 1205.0,
     '5-6-3': 1279.0,
     '5-6-4': 1724.0,
     '6-1-2': 2320.0,
     '6-1-3': 2257.0,
     '6-1-4': 2921.0,
     '6-1-5': 1786.0,
     '6-2-1': 4070.0,
     '6-2-3': 4514.0,
     '6-2-4': 5643.0,
     '6-2-5': 2921.0,
     '6-3-1': 3598.0,
     '6-3-2': 4774.0,
     '6-3-4': 4433.0,
     '6-3-5': 2387.0,
     '6-4-1': 4514.0,
     '6-4-2': 6534.0,
     '6-4-3': 4138.0,
     '6-4-5': 4004.0,
     '6-5-1': 2559.0,
     '6-5-2': 2698.0,
     '6-5-3': 4070.0,
     '6-5-4': 4774.0,
     'date': '2021-08-12',
     'race': 1,
     'stadium': 10,
     'update': '締切時オッズ'}
    ```

    </details>

- To get the oods of trio （三連複） of the race in the stadioum on the day:

  - API:

    - ```python
      PyJPBoatrace().get_odds_trio(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().Trio.get(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_odds_trio(date(2021, 8, 12), 10, 1))
    {'1=2=3': 5.1,
     '1=2=4': 14.6,
     '1=2=5': 4.7,
     '1=2=6': 73.8,
     '1=3=4': 5.9,
     '1=3=5': 2.5,
     '1=3=6': 73.8,
     '1=4=5': 6.4,
     '1=4=6': 106.6,
     '1=5=6': 59.0,
     '2=3=4': 98.4,
     '2=3=5': 36.2,
     '2=3=6': 295.3,
     '2=4=5': 93.6,
     '2=4=6': 426.5,
     '2=5=6': 159.9,
     '3=4=5': 45.7,
     '3=4=6': 548.4,
     '3=5=6': 191.9,
     '4=5=6': 213.2,
     'date': '2021-08-12',
     'race': 1,
     'stadium': 10,
     'update': '締切時オッズ'}
    ```

    </details>

- To get the just-before information, e.g. weather and start-timing, of the race in the stadioum on the day:

  - API:

    - ```python
      PyJPBoatrace().get_just_before_info(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().JustBeforeInfo.get(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_just_before_info(date(2021, 8, 12), 10, 1))
    {'boat1': {'display_time': 6.77,
               'name': '武田光史',
               'parts_exchange': [],
               'previous_race': {},
               'propeller': '',
               'tilt': -0.5,
               'weight': 52.6,
               'weight_adjustment': 0.0},
     'boat2': {'display_time': 6.76,
               'name': '大澤誠也',
               'parts_exchange': [],
               'previous_race': {},
               'propeller': '',
               'tilt': -0.5,
               'weight': 53.1,
               'weight_adjustment': 0.0},
     'boat3': {'display_time': 6.77,
               'name': '堀本裕也',
               'parts_exchange': [],
               'previous_race': {},
               'propeller': '',
               'tilt': -0.5,
               'weight': 50.0,
               'weight_adjustment': 2.0},
     'boat4': {'display_time': 6.77,
               'name': '信濃由行',
               'parts_exchange': [],
               'previous_race': {},
               'propeller': '',
               'tilt': -0.5,
               'weight': 52.3,
               'weight_adjustment': 0.0},
     'boat5': {'display_time': 6.79,
               'name': '木田峰由季',
               'parts_exchange': [],
               'previous_race': {},
               'propeller': '',
               'tilt': -0.5,
               'weight': 52.2,
               'weight_adjustment': 0.0},
     'boat6': {'display_time': 6.81,
               'name': '加藤優弥',
               'parts_exchange': [],
               'previous_race': {},
               'propeller': '',
               'tilt': -0.5,
               'weight': 52.6,
               'weight_adjustment': 0.0},
     'date': '2021-08-12',
     'race': 1,
     'stadium': 10,
     'start_display': {'course1': {'ST': 0.11, 'boat': 1},
                       'course2': {'ST': 0.13, 'boat': 2},
                       'course3': {'ST': 0.22, 'boat': 3},
                       'course4': {'ST': 0.17, 'boat': 4},
                       'course5': {'ST': 0.11, 'boat': 5},
                       'course6': {'ST': 0.13, 'boat': 6}},
     'weather_information': {'direction': 14,
                             'temperature': 25.0,
                             'time': '14:53現在',
                             'water_temperature': 27.0,
                             'wave_height': 1.0,
                             'weather': '曇り',
                             'wind_direction': 2,
                             'wind_speed': 1.0}}
    ```

    </details>

- To get the race result of the race in the stadioum on the day:

  - API:

    - ```python
      PyJPBoatrace().get_race_result(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

    - ```python
      PyJPBoatrace().Result.get(d: datetime.date, stadium: int, race: int) -> Dict[str, Any]
      ```

  - Return:
    <details>
    <summary> Sample </summary>

    ```python
    >>> from pyjpboatrace import PyJPBoatrace
    >>> from datetime import date
    >>> from pprint import pprint
    >>> pprint(PyJPBoatrace().get_race_result(date(2021, 8, 12), 10, 1))
    {'date': '2021-08-12',
     'kimarite': '逃げ',
     'note': [],
     'payoff': {'exacta': {'payoff': 400, 'popularity': 2, 'result': '1-5'},
                'exacta_all': [{'payoff': 400, 'popularity': 2, 'result': '1-5'}],
                'place_show': [{'payoff': 100, 'popularity': '', 'result': '1'},
                               {'payoff': 150, 'popularity': '', 'result': '5'}],
                'place_show_all': [{'payoff': 100, 'popularity': '', 'result': '1'},
                                   {'payoff': 150,
                                    'popularity': '',
                                    'result': '5'}],
                'quinella': {'payoff': 440, 'popularity': 2, 'result': '1=5'},
                'quinella_all': [{'payoff': 440, 'popularity': 2, 'result': '1=5'}],
                'quinella_place': [{'payoff': 110,
                                    'popularity': 2,
                                    'result': '1=5'},
                                   {'payoff': 110,
                                    'popularity': 1,
                                    'result': '1=3'},
                                   {'payoff': 190,
                                    'popularity': 4,
                                    'result': '3=5'}],
                'quinella_place_all': [{'payoff': 110,
                                        'popularity': 2,
                                        'result': '1=5'},
                                       {'payoff': 110,
                                        'popularity': 1,
                                        'result': '1=3'},
                                       {'payoff': 190,
                                        'popularity': 4,
                                        'result': '3=5'}],
                'trifecta': {'payoff': 730, 'popularity': 2, 'result': '1-5-3'},
                'trifecta_all': [{'payoff': 730,
                                  'popularity': 2,
                                  'result': '1-5-3'}],
                'trio': {'payoff': 250, 'popularity': 1, 'result': '1=3=5'},
                'trio_all': [{'payoff': 250, 'popularity': 1, 'result': '1=3=5'}],
                'win': {'payoff': 100, 'popularity': '', 'result': '1'},
                'win_all': [{'payoff': 100, 'popularity': '', 'result': '1'}]},
     'race': 1,
     'result': [{'boat': 1,
                 'name': '武田光史',
                 'racerid': 3654,
                 'rank': 1,
                 'time': '1\'49"2'},
                {'boat': 5,
                 'name': '木田峰由季',
                 'racerid': 4587,
                 'rank': 2,
                 'time': '1\'50"8'},
                {'boat': 3,
                 'name': '堀本裕也',
                 'racerid': 3895,
                 'rank': 3,
                 'time': '1\'52"6'},
                {'boat': 2,
                 'name': '大澤誠也',
                 'racerid': 5074,
                 'rank': 4,
                 'time': '1\'54"1'},
                {'boat': 6, 'name': '加藤優弥', 'racerid': 5185, 'rank': 5, 'time': ''},
                {'boat': 4,
                 'name': '信濃由行',
                 'racerid': 3620,
                 'rank': 6,
                 'time': ''}],
     'return': [],
     'stadium': 10,
     'start_information': {'course1': {'ST': 0.26, 'boat': 1},
                           'course2': {'ST': 0.25, 'boat': 2},
                           'course3': {'ST': 0.23, 'boat': 3},
                           'course4': {'ST': 0.25, 'boat': 4},
                           'course5': {'ST': 0.21, 'boat': 5},
                           'course6': {'ST': 0.17, 'boat': 6}},
     'weather_information': {'direction': 14,
                             'temperature': 27.0,
                             'water_temperature': 26.0,
                             'wave_height': 1,
                             'weather': '曇り',
                             'wind_direction': 12,
                             'wind_speed': 1}}
    ```

    </details>

  - NOTE: you may be confused by the output of `PyJPBoatrace().get_race_result` because the contents of "payoff" key in the output have the following keys:

    - "exacta"
    - "exacta_all"
    - "place_show"
    - "place_show_all"
    - "quinella"
    - "quinella_all"
    - "quinella_place"
    - "quinella_place_all"
    - "trifecta"
    - "trifecta_all"
    - "trio"
    - "trio_all"
    - "win"
    - "win_all"

    For "win", "exacta", "quinella", "trifecta" and "trio", the difference between a key without "all" footer and a key with "all" footer is that the former means ONE result while the latter means ALL results.
    For example, if "1-2-3" and "1-2-4" is hit as trifecta in a race, that is, if 3rd boat and 4th boat are tied for third place, the valud of "trifecta" key is `{'payoff': ..., 'popularity': ..., 'result': '1-2-3'}` while the value of "trifecta_all" key is `[{'payoff': ..., 'popularity': ..., 'result': '1-2-3'}, {'payoff': ..., 'popularity': ..., 'result': '1-2-4'}]`.
    On the other hand, for "place_show" and "quinella_place", there is no difference between a key without "all" footer and a key with "all" footer.

These functions return `dict` object.

#### Operations

- To deposit money for betting (Unit: 1,000 yen):
  - API
    - `PyJPBoatrace().deposit(num_of_thousands_yen: int) -> None`
    - `PyJPBoatrace().Deposit.do(num_of_thousands_yen: int) -> None`
  - Return:
    - Nothing
- To get the limit of betting amount, that is, your current deposit:
  - API
    - `PyJPBoatrace().get_bet_limit() -> int`
    - `PyJPBoatrace().BettingLimitCheck.do() -> int`
  - Return:
    - `int`: the amount of deposit
- To withdraw your current deposit:

  - API:

    - `PyJPBoatrace().withdraw() -> None`
    - `PyJPBoatrace().Widthdraw.do() -> None`

  - Return:
    - Nothing

- To bet some tickets.

  - API:

    - ```python
      PyJPBoatrace().bet(
        stadium:int,
        race:int,
        trifecta_betting_dict: Dict[str, int],
        trio_betting_dict: Dict[str, int],
        exacta_betting_dict: Dict[str, int],
        quinela_betting_dict: Dict[str, int],
        quinellaplace_betting_dict: Dict[str, int],
        win_betting_dict: Dict[str, int],
        placeshow_betting_dict: Dict[str, int],
      ) -> bool
      ```

    - ```python
      PyJPBoatrace().Bet.do(
        stadium:int,
        race:int,
        trifecta_betting_dict: Dict[str, int],
        trio_betting_dict: Dict[str, int],
        exacta_betting_dict: Dict[str, int],
        quinela_betting_dict: Dict[str, int],
        quinellaplace_betting_dict: Dict[str, int],
        win_betting_dict: Dict[str, int],
        placeshow_betting_dict: Dict[str, int],
      ) -> bool
      ```

  - Each dictionary consits of pairs of winning numbers and betting amount, e.g., `{'1-2-3':100}` for trifecta_betting_dict

IMPORTANT NOTE: you must give a driver other than `HTTPGetDriver` to use above actions.

### Demo

#### Demo 1 : Getting odds data

The following example is useful.
Suppose that you want get the odds of trifecta of 4th race in stadium "桐生" on 2020/12/02 and dump the result into `data.json`.

```python
from datetime import date
import json
from pyjpboatrace import PyJPBoatrace

# initialize
boatrace_tools = PyJPBoatrace()

# get data
dic = boatrace_tools.get_odds_trifecta(d=date(2020,12,2), stadium=1, race=4)

# dump data
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dic, f, ensure_ascii=False)

# close (you can use 'with' statement)
boatrace_tools.close()
```

You can get many kinds of data as this example.

#### Demo 2 : Betting

Suppose it is 2020/12/02 and you want to bet 200 yen on trifecta 1-3-4 and 100 yen on trio 1=3=4 in the 2nd race in stadium "桐生" on 2020/12/02. NOTE: you need google chrome in the following example.

```python
from datetime import date
from pyjpboatrace import PyJPBoatrace
from pyjpboatrace.drivers import create_chrome_driver
from pyjpboatrace.const import STADIUMS_MAP
from pyjpboatrace.user_information import UserInformation

# initialize
user = UserInformation(
    userid='YOUR_USER_ID',
    pin='YOUR_PIN',
    auth_pass='YOUR_AUTHENTIFICATION_PASSWORD',
    vote_pass='YOUR_BETTING_PASSWORD',
)
boatrace_tools = PyJPBoatrace(
    driver=create_chrome_driver(),
    user_information=user
)

# deposit 1,000 yen
boatrace_tools.deposit(1)

# bet
stadium = {s:i for i,s in STADIUMS_MAP}.get("桐生")
race = 2
boatrace_tools.bet(
    stadium=stadium,
    race=race,
    trifecta_betting_dict={'1-3-4':200},
    trio_betting_dict={'1=3=4':100}
)

# waiting for the race result ...

# withdraw
boatrace_tools.withdraw()

# close (you can use 'with' statement)
boatrace_tools.close()
```

### NOTE

The map between integers and stadiums is given by `STADIUMS_MAP` in `pyjpboatrace.const`.

## Contribution Guide

### Requirement

- Python >= 3.9
  - uv
- Chrome
- Firefox
- bash
- curl

### Issues

- For any bugs, use [BUG REPORT](https://github.com/hmasdev/pyjpboatrace/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D) to create an issue.

- For any enhancement, use [FEATURE REQUEST](https://github.com/hmasdev/pyjpboatrace/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=) to create an issue.

- For other topics, create an issue with a clear and concise description.

### Pull Request

1. Fork ([https://github.com/hmasdev/pyjpboatrace/fork](https://github.com/hmasdev/pyjpboatrace/fork));
2. Create your feature branch (`git checkout -b feautre/xxxx`);
3. Test codes according to [Test Subsection](#HowToTestAnchor);
4. Commit your changes (`git commit -am 'Add xxxx feature`);
5. Push to the branch (`git push origin feature/xxxx`);
6. Create new Pull Request

### Setup the develop environment

First, fork this repository and clone it to your local machine.

```bash
git clone https://github.com/hmasdev/pyjpboatrace/
cd pyjpboatrace
```

Then, create your development environment with `uv`.

```bash
uv sync --dev
```

### Test

<div id="HowToTestAnchor"></div>

You can do unit tests and integration tests as follows:

```bash
./download_html_for_test.sh  # Only 1 time
uv run pytest -m "not integrate and not spending_money" # unit tests
uv run pytest # unit tests and integration tests
```

`pytest` does not test depositing, withdrawing or betting.
If you want to test them, make `.secrets.json` at first:

```json
{
  "userid": "YOUR_USER_ID",
  "pin": "YOUR_PIN",
  "auth_pass": "YOUR_AUTHENTIFICATION_PASSWORD",
  "vote_pass": "YOUR_BETTING_PASSWORD"
}
```

Then, run

```bash
uv run pytest -m "spending_money"
```

WARNING: Tests with `spending_money` spend 700 yen.

### Check the format of code and static types

You should execute the following codes to check the format of code and static types:

```bash
uv run ruff check pyjpboatrace tests
uv run mypy pyjpboatrace tests
```

### How to Update README.md

To update the content of [README.md](./README.md), please do not edit the file directly.
Instead, make your changes to [README.md.j2](./README.md.j2).

After making updates to `README.md.j2`, execute the following command to regenerate `README.md`:

```bash
uv run update_readme.py > README.md
```

This process is necessary because README.md is dynamically generated from the README.md.j2 template.
Direct modifications to README.md will be lost, as they are automatically overwritten by an automated process whenever the template is updated.

Remember, to preserve your changes, always update README.md.j2 and not README.md directly.

## LICENSE

[MIT](https://github.com/hmasdev/pyjpboatrace/tree/main/LICENSE)

## Authors

[hmasdev](https://github.com/hmasdev)
