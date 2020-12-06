# PyJPBoatRace: Python-based Japanese boatrace tools

![GitHub top language](https://img.shields.io/github/languages/top/hmasdev/pyjpboatrace?style=plastic)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hmasdev/pyjpboatrace?sort=semver&style=plastic)
![GitHub](https://img.shields.io/github/license/hmasdev/pyjpboatrace?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/hmasdev/pyjpboatrace?style=plastic)
[![](https://github.com/hmasdev/pyjpboatrace/workflows/Pytest/badge.svg?branch=main&event=push)](https://github.com/hmasdev/pyjpboatrace/actions?query=workflow%3APytest)

Japanese boat race is extremely exciting sports.
It is also fun to predict the results of races.
Prediction like machine learning method requires data.
Thus, this package provides you with useful tools for data analysis for boatrace.

## Installation

### Dependencies

- python >= 3.7
- requests >= 2.25.0
- beautifulsoup4 >= 4.9.3

### User installation

```
    pip install -U pyjpboatrace
```

## How to use

### Functions

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

### Demo

The following example is useful.
Suppose the you want get the odds of trifecta of 4th race in stadium "桐生" on 2020/12/02 and dump the result into `data.json`.

```python
from datetime import date
import json
from pyjpboatrace import PyJPBoatrace

boatrace_tools = PyJPBoatrace()

dic = boatrace_tools.get_odds_trifecta(d=date(2020,12,2), stadium=1, race=4)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dic, f, ensure_ascii=False)
```

### NOTE

The map between integers and stadiums is defined as `STADIUMS_MAP` in `const.py`.

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
