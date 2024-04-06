from datetime import date
from jinja2 import FileSystemLoader, Environment
import pprint
from pyjpboatrace import PyJPBoatrace

readme = Environment(loader=FileSystemLoader('.')).get_template('README.md.j2')


def format_example_output(output_dict: dict) -> str:
    return pprint.pformat(output_dict).replace('\n', '\n    ')


examples = {
    'get_stadiums': {
        'command': 'PyJPBoatrace().get_stadiums(date(2021, 8, 12))',  # noqa
        'output': format_example_output(PyJPBoatrace().get_stadiums(date(2021, 8, 12))),  # noqa
    },
    'get_12races': {
        'command': 'PyJPBoatrace().get_12races(date(2021, 8, 12), 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_12races(date(2021, 8, 12), 1)),  # noqa
    },
    'get_race_info': {
        'command': 'PyJPBoatrace().get_race_info(date(2021, 8, 12), 10, 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_race_info(date(2021, 8, 12), 10, 1)),  # noqa
    },
    'get_odds_win_placeshow': {
        'command': 'PyJPBoatrace().get_odds_win_placeshow(date(2021, 8, 12), 10, 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_odds_win_placeshow(date(2021, 8, 12), 10, 1)),  # noqa
    },
    'get_odds_quinellaplace': {
        'command': 'PyJPBoatrace().get_odds_quinellaplace(date(2021, 8, 12), 10, 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_odds_quinellaplace(date(2021, 8, 12), 10, 1)),  # noqa
    },
    'get_odds_exacta_quinella': {
        'command': 'PyJPBoatrace().get_odds_exacta_quinella(date(2021, 8, 12), 10, 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_odds_exacta_quinella(date(2021, 8, 12), 10, 1)),  # noqa
    },
    'get_odds_trifecta': {
        'command': 'PyJPBoatrace().get_odds_trifecta(date(2021, 8, 12), 10, 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_odds_trifecta(date(2021, 8, 12), 10, 1)),  # noqa
    },
    'get_odds_trio': {
        'command': 'PyJPBoatrace().get_odds_trio(date(2021, 8, 12), 10, 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_odds_trio(date(2021, 8, 12), 10, 1)),  # noqa
    },
    'get_just_before_info': {
        'command': 'PyJPBoatrace().get_just_before_info(date(2021, 8, 12), 10, 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_just_before_info(date(2021, 8, 12), 10, 1)),  # noqa
    },
    'get_race_result': {
        'command': 'PyJPBoatrace().get_race_result(date(2021, 8, 12), 10, 1)',  # noqa
        'output': format_example_output(PyJPBoatrace().get_race_result(date(2021, 8, 12), 10, 1)),  # noqa
    },
}

print(readme.render(**examples))
