import json
import os
from typing import Any, Dict

EXPECTED_DIREC = 'tests/data'
MOCK_HTML_DIREC = 'tests/mock_html'


def get_expected_json(
    fname: str,
    direc: str = EXPECTED_DIREC
) -> Dict[str, Any]:
    f"""load expected json

    Args:
        fname (str): file name
        direc (str, optional): directory name. Defaults to {EXPECTED_DIREC}.

    Returns:
        Dict[str, Any]: expected data
    """
    path = os.path.join(direc, fname)
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def get_mock_html(
    fname: str,
    direc: str = MOCK_HTML_DIREC,
) -> str:
    f"""load html file

    Args:
        fname (str): file name
        direc (str, optional): directory name. Defaults to {MOCK_HTML_DIREC}.

    Returns:
        str: HTML
    """
    path = os.path.join(direc, fname)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
