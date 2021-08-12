# PyJPBoatRace: Python-based Japanese boatrace tools :speedboat:

![GitHub top language](https://img.shields.io/github/languages/top/hmasdev/pyjpboatrace)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hmasdev/pyjpboatrace?sort=semver)
![GitHub](https://img.shields.io/github/license/hmasdev/pyjpboatrace)
![GitHub last commit](https://img.shields.io/github/last-commit/hmasdev/pyjpboatrace)

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

- python >= 3.7
- requests>=2.25.0
- beautifulsoup4>=4.9.3
- selenium>=3.141.0
- webdriver-manager>=3.2.2
- msedge-selenium-tools

### User installation

```
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
    {
      "date": "2021-08-12",
      "大村":{
        "status":"-",
        "grade":[
          "ippan",
          "rookie"
        ],
        "timeframe":"nighter",
        "title":"ルーキーシリーズ第１６戦　オール進入固定レース",
        "period":[
          "2020-09-07",
          "2020-09-13"
        ],
        "day":"初日"
      },
      ...
    }
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
    {
      "date": "2021-08-12",
      "stadium": 1,
      "1R":{
          "vote_limit":"2020-01-01 10:00:00",
          "status":"発売終了",
          "racers":{
              "boat1":{
                  "name":"Name1",
                  "class":"A1"
              },
              "boat2":{
                  "name":"Name2",
                  "class":"A2"
              },
              "boat3":{
                  "name":"Name3",
                  "class":"B1"
              },
              "boat4":{
                  "name":"Name4",
                  "class":"B2"
              },
              "boat5":{
                  "name":"Name5",
                  "class":"A1"
              },
              "boat6":{
                  "name":"Name6",
                  "class":"B1"
              }
          }
      },
      ...,
      "12R":{
          "vote_limit":"2020-01-01 15:30:00",
          "status":"発売終了",
          "racers":{
              "boat1":{
                  "name":"Name1",
                  "class":"A1"
              },
              "boat2":{
                  "name":"Name2",
                  "class":"A2"
              },
              "boat3":{
                  "name":"Name3",
                  "class":"B1"
              },
              "boat4":{
                  "name":"Name4",
                  "class":"B2"
              },
              "boat5":{
                  "name":"Name5",
                  "class":"A1"
              },
              "boat6":{
                  "name":"Name6",
                  "class":"B1"
              }
          }
      }
    }
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
    {
      "date": "2021-08-12",
      "stadium": 10,
      "race": 1,
      "boat1": {
        "racerid": 9999,
        "class": "A1",
        "name": "Name1",
        "branch": "Somewhere",
        "birthplace": "Somewhere",
        "age": 40,
        "weight": 53.2,
        "F": 0,
        "L": 0,
        "aveST": 0.19,
        "global_win_pt": 6.43,
        "global_in2nd": 43.86,
        "global_in3rd": 68.42,
        "local_win_pt": 0,
        "local_in2nd": 0,
        "local_in3rd": 0,
        "motor": 42,
        "motor_in2nd": 35.48,
        "motor_in3rd": 56.13,
        "boat": 41,
        "boat_in2nd": 30.77,
        "boat_in3rd": 54.49,
        "result": [
          {
              "race": 8,
              "boat": 2,
              "course": 2,
              "ST": 0.24,
              "rank": 6
          },
          {},
          {
              "race": 4,
              "boat": 4,
              "course": 4,
              "ST": 0.28,
              "rank": 5
          },
          ...,
          {}
        ]
      },
      ...,
      "race_title": [
          "みくにあさガチ",
          "1800m"
      ]
    }
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
    {
      "date": "2020-10-24",
      "stadium": 14,
      "race": 1,
      "win":{
        "1": 1.0,
        "2": 6.8,
        "3": 9.3,
        "4": 41.3,
        "5": 36.1,
        "6": 72.3
      },
      "place_show":{
        "1": [1.0, 1.3],
        "2": [3.3, 5.0],
        "3": [1.5, 2.2],
        "4": [5.7, 8.9],
        "5": [1.1, 1.6],
        "6": [22.0, 33.3]
      },
      "update": "締切時オッズ"
    }
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
    {
      "date": "2020-10-24",
      "stadium": 14,
      "race": 1,
      "1=2": [1.2,1.4],
      "1=3": [1.3,1.8],
      ...,
      "5=6": [27.2,30.9],
      "update": "9:02"
    }
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
    {
      "date": "2020-10-24",
      "stadium": 14,
      "race": 1,
      "exacta":{
        "1-2": 2.5,
        "1-3": 2.8,
        ...,
        "6-5": 2931.0
      },
      "quinella":{
        "1=2": 3.0,
        "1=3": 2.1,
        ...,
        "5=6": 298.3
      },
      "update": "12:30"
    }
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
    {
      "date": "2020-10-24",
      "stadium": 14,
      "race": 1,
      "1-2-3": 5.6,
      "1-2-4": 14.4,
      ...,
      "6-5-4": 8650.0,
      "update": "締切時オッズ"
    }
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
    {
      "date": "2020-10-24",
      "stadium": 14,
      "race": 1,
      "1=2=3": "欠場",
      "1=2=4": "欠場",
      "1=2=5": "欠場",
      "1=2=6": "欠場",
      "1=3=4": "欠場",
      "2=3=4": 4.2,
      "1=3=5": "欠場",
      "2=3=5": 30,
      "1=3=6": "欠場",
      "2=3=6": 2.3,
      "1=4=5": "欠場",
      "2=4=5": 25,
      "3=4=5": 79.2,
      "1=4=6": "欠場",
      "2=4=6": 1.9,
      "3=4=6": 60,
      "1=5=6": "欠場",
      "2=5=6": 26.7,
      "3=5=6": 132.1,
      "4=5=6": 90.1,
      "update": "15:30"
    }
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
    {
      "date": "2020-08-25",
      "stadium": 14,
      "race": 7,
      "boat1":{
          "name":"Name1",
          "weight":55.1,
          "weight_adjustment":0.0,
          "display_time":6.87,
          "tilt":0.0,
          "propeller":"",
          "parts_exchange":[
              "リング×１",
              "シャフト"
          ],
          "previous_race":{}
      },
      ...,
      "boat6":{
          "name":"Name6",
          "weight":51.0,
          "weight_adjustment":0.0,
          "display_time":6.88,
          "tilt":-0.5,
          "propeller":"",
          "parts_exchange":[],
          "previous_race":{
              "race":3,
              "boat":3,
              "course":3,
              "ST":0.13,
              "rank":6
          }
      },
      "start_display":{
          "course1":{
              "boat":1,
              "ST":0.02
          },
          ...,
          "course6":{
              "boat":6,
              "ST":0.10
          }
      },
      "weather_information":{
          "direction":16,
          "weather":"晴",
          "temperature":31.0,
          "wind_direction":14,
          "wind_speed":5,
          "water_temperature":27.0,
          "wave_height":5,
          "time":"6R時点"
      }
    }
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
    {
      "date": "2020-10-24",
      "stadium": 14,
      "race": 1,
      "result":[
          {
              "rank":1,
              "boat":1,
              "name":"WHO1",
              "racerid":9999,
              "time":"1'50\"0"
          },
          ...,
          {
              "rank":6,
              "boat":2,
              "name":"WHO6",
              "racerid":8888,
              "time":""
          }
      ],
      "kimarite":"逃げ",
      "start_information":{
          "course1":{
              "boat":1,
              "ST":0.05
          },
          ...,
          "course6":{
              "boat":6,
              "ST":0.11
          }
      },
      "payoff":{
          "trifecta":{
              "result":"1-5-6",
              "payoff":12345,
              "popularity":34
          },
          ...,
          "quinella_place":[
              {
                  "result":"1=5",
                  "payoff":220,
                  "popularity":3
              },
              ...
          ],
          ...,
      },
      "weather_information":{
          "direction":16,
          "weather":"晴",
          "temperature":17.0,
          "wind_direction":6,
          "wind_speed":5,
          "water_temperature":21.0,
          "wave_height":5
      },
      "return":[],
      "note":[]
    }
    ```

    </details>

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

- Python >= 3.7
- Pipenv (You can install pipenv by `pip install pipenv`)
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

### Test

<div id="HowToTestAnchor"></div>

You can do unit tests and integration tests as follows:

```bash
$ ./download_html_for_test.sh  # Only 1 time
$ pipenv run pytest -m "not integrate and not spending_money" # unit tests
$ pipenv run pytest  # unit tests and integration tests
```

`pipenv run pytest` does not test depositing, withdrawing or betting.
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
$ pipenv run pytest -m "spending_money"
```

WARNING: Tests with `spending_money` spend 700 yen.

## LICENSE

[MIT](https://github.com/hmasdev/pyjpboatrace/tree/main/LICENSE)

## Authors

[hmasdev](https://github.com/hmasdev)
