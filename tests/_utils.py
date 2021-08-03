from typing import Any, Callable, Dict


def create_side_effect(
    dic: Dict[str, Any],
    default_value: Any = None,
) -> Callable[..., Any]:
    """Create a side effect of mock

    Args:
        dic (Dict[str, Any]): Argument-Return Map
        default_value (Any, optional): Default return. Defaults to None.

    Returns:
        Callable[..., Any]: side-effect function
    """
    return lambda arg: dic.get(arg, default_value)
