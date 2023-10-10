from typing import Any, Dict
import json
from datetime import datetime
from functools import lru_cache
import os
import pytz
from typing import Callable, Optional
from pyjpboatrace.const import BOATRACE_START, BOATRACE_END
from pyjpboatrace.user_information import UserInformation


def create_side_effect(
    dic: Dict[tuple, Any],
    default_value: Any = None,
) -> Callable[..., Any]:
    """Create a side effect of mock

    Args:
        dic (Dict[tuple, Any]): Argument-Return Map
        default_value (Any, optional): Default return. Defaults to None.

    Returns:
        Callable[..., Any]: side-effect function
    """
    return lambda *arg: dic.get(arg, default_value)


def is_boatrace_time() -> bool:
    return BOATRACE_START <= datetime.now(pytz.timezone("Asia/Tokyo")).time() <= BOATRACE_END  # noqa


@lru_cache(maxsize=1)
def get_user_info(secretsjson="./.secrets.json") -> Optional[UserInformation]:
    # TODO use pytest.fixture
    if os.path.exists(secretsjson):
        return UserInformation(json_file=secretsjson)
    else:
        return None


def get_expected_json(
    fname: str,
    direc: str = 'tests/data',
) -> Dict[str, Any]:
    """load expected json

    Args:
        fname (str): file name
        direc (str, optional): directory name. Defaults to tests/data.

    Returns:
        Dict[str, Any]: expected data
    """
    path = os.path.join(direc, fname)
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def get_mock_html(
    fname: str,
    direc: str = 'tests/mock_html',
) -> str:
    """load html file

    Args:
        fname (str): file name
        direc (str, optional): directory name. Defaults to tests/mock_html.

    Returns:
        str: HTML
    """
    path = os.path.join(direc, fname)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
