from typing import Any
from typing import Iterable
from typing import Type
from typing import Union

from glom import glom as _glom
from glom import GlomError
from glom import Spec
from pydantic import ValidationError

from ps_watch.exceptions import PSWatchDataError
from ps_watch.exceptions import PSWatchValidationError
from ps_watch.models import PSItem
from ps_watch.models import PSProfile


def glom(data: Iterable, spec: Union[str, dict, tuple, list, Spec]) -> Any:
    try:
        return _glom(data, spec)
    except GlomError as e:
        raise PSWatchDataError(e, data)


def serialize(
    model: Union[Type[PSProfile], Type[PSItem]], data: dict, **kwargs
) -> Union[PSProfile, PSItem]:
    data.update(kwargs)
    try:
        return model.parse_obj(data)
    except ValidationError as e:
        raise PSWatchValidationError(e, data)
