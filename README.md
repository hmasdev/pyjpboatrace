# PyJPBoatRace: Python-based Japanese boatrace tools

![GitHub top language](https://img.shields.io/github/languages/top/hmasdev/pyjpboatrace)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hmasdev/pyjpboatrace?sort=semver)
![GitHub](https://img.shields.io/github/license/hmasdev/pyjpboatrace)
![GitHub last commit](https://img.shields.io/github/last-commit/hmasdev/pyjpboatrace)

Japanese boat race is extremely exciting sports.
It is also fun to predict the results of races.
Prediction like machine learning method requires data.
Thus, this package provides you with useful tools for data analysis and auto-betting for boatrace.

## Installation

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

1. (optional) create an instance of UserInformation [^1]
2. (optional) create a selenium driver [^1]
3. create an instance of PyJPBoatrace
4. execute functions and actions

[^1]: you must create a UserInformation instance and a selenium driver to order to deposit, withdraw or bet.

### UserInformation

- `pyjpboatrace.user_information.UserInformation(userid:str,pin:str,auth_pass:str, vote_pass:str, json_file:str)`

NOTE: If you use a json file to create an instance of UserInformation, the json file contains the following keys: userid, pin, auth_pass and vote_pass.

### Selenium Driver

You can use the following functions to create selenium drivers:

- pyjpboatrace.drivers.create_chrome_driver()
- pyjpboatrace.drivers.create_firefox_driver()
- pyjpboatrace.drivers.create_edge_driver()
- pyjpboatrace.drivers.create_httpget_driver()

NOTE 1: you can use your own selenium driver.

NOTE 2: If you use create_httpget_driver, you cannot execute actions, e.g. deposit, withdraw or bet.

### Functions and actions

#### Functions

- `PyJPBoatrace().get_stadiums(d:datetime.date)`
  - To get a list of stadiums which hold races on the given day.
- `PyJPBoatrace().get_12races(d:datetime.date, stadium:int)`
  - To get 12 races held in the given stadium on the given day.
- `PyJPBoatrace().get_race_info(d:datetime.date, stadium:int, race:int)`
  - To get the basic information of the race in the stadium on a day.
- `PyJPBoatrace().get_odds_win_placeshow(d:datetime.date, stadium:int, race:int)`
  - To get the odds of win (単勝) and place-show (複勝) of the race in the stadium on the day.
- `PyJPBoatrace().get_odds_quinellaplace(d:datetime.date, stadium:int, race:int)`
  - To get the odds of quinella place (拡連複) of the race in the stadioum on the day.
- `PyJPBoatrace().get_odds_exacta_quinella(d:datetime.date, stadium:int, race:int)`
  - To get the odds of exacta (二連単) and quinella (二連複) of the race in the stadioum on the day.
- `PyJPBoatrace().get_odds_trifecta(d:datetime.date, stadium:int, race:int)`
  - To get the odds of trifecta (三連単) of the race in the stadioum on the day.
- `PyJPBoatrace().get_odds_trio(d:datetime.date, stadium:int, race:int)`
  - To get the oods of trio （三連複） of the race in the stadioum on the day.
- `PyJPBoatrace().get_just_before_info(d:datetime.date, stadium:int, race:int)`
  - To get the just-before information, e.g. weather and start-timing, of the race in the stadioum on the day.
- `PyJPBoatrace().get_race_result(d:datetime.date, stadium:int, race:int)`
  - To get the race result of the race in the stadioum on the day.

These functions return `dict` object.

#### Actions

- `PyJPBoatrace().deposit(num_of_thousands_yen:int) -> None`
  - To deposit money for betting. (Unit: 1,000 yen)
- `PyJPBoatrace().get_bet_limit() -> None`
  - To get the limit of betting amount, that is, your current deposit.
- `PyJPBoatrace().withdraw() -> None`
  - To withdraw your current deposit.
- `PyJPBoatrace().bet(place:int, race:int, trifecta_betting_dict:dict, trio_betting_dict:dict, exacta_betting_dict:dict, quinela_betting_dict:dict, quinellaplace_betting_dict:dict, win_betting_dict:dict, placeshow_betting_dict:dict) -> bool`
  - To bet some tickets.
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

Suppose it is 2020/12/02 and you want to bet 200 yen on trifecta 1-3-4 and 100 yen on trio 1=3=4 in the 2nd race in stadium "桐生" on 2020/12/02. NOTE: you need google chrome.

```python
from datetime import date
from pyjpboatrace import PyJPBoatrace
from pyjpboatrace.drivers import create_chrome_driver
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
place = 1
race = 2
boatrace_tools.bet(
    place=place,
    race=race,
    trifecta_betting_dict={'1-3-4':200},
    trio_betting_dict={'1=3=4':100}
)

# waiting for the race result

# withdraw
boatrace_tools.withdraw()

# close (you can use 'with' statement)
boatrace_tools.close()
```

### NOTE

The map between integers and stadiums is given by `STADIUMS_MAP` in `const.py`.

## Contribution

1. Fork ([https://github.com/hmasdev/pyjpboatrace/fork](https://github.com/hmasdev/pyjpboatrace/fork));
2. Create your feature branch (`git checkout -b feautre/xxxx`);
3. Commit your changes (`git commit -am 'Add xxxx feature`);
4. Push to the branch (`git push origin feature/xxxx`)
5. Create new Pull Request

## LICENSE

[MIT](https://github.com/hmasdev/pyjpboatrace/tree/main/LICENSE)

## Authors

[hmasdev](https://github.com/hmasdev)
