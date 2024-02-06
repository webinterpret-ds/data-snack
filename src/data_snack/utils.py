from typing import Iterable, Any


def get_attribute_of_first_element_from_iterable(iterable: Iterable, attribute_name: str) -> Any:
    return getattr(next(iter(iterable), None), attribute_name, None)
