"""
The core decorator logic
"""

import json
import inspect
from typing import Callable, Any, Dict
from .exceptions import LoggerNonSerializableError


def _get_func_args(
    func: Callable[..., Any], *args: Any, **kwargs: Any
) -> Dict[str, Any]:
    """
    Maps all positonal and keyword arguments to their parameter names.

    We need to capture the name of the arguements (e.g., max_depth) and not just their values (e.g., 5).
    This function handles the logic of binding *args and **kwargs to the function signature.

    :param func: The function called.
    :param args: The positional arguments passed to the function.
    :param kwargs: The keyword arguements passed to the function.
    :return: A dictionary of parameter names mapped to their values.
    """
    try:
        # Bind the positional and keyword arguments to the function signature
        bound_args = inspect.signature(func).bind(*args, **kwargs)
        # Apply the default for any missing arguements
        bound_args.apply_defaults()
        # Arguments is an OrderedDict, we convert it into plain dict
        return dict(bound_args.arguments)
    except Exception:
        # Fallback for complex callables where binding might fail.
        # this is less informative but safer than crashing.
        return {"args": args, "kwargs": kwargs}
