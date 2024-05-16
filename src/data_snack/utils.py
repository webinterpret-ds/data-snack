from typing import Any, Iterable


def get_attribute_of_first_element_from_iterable(iterable: Iterable, attribute_name: str) -> Any:
    return getattr(next(iter(iterable), None), attribute_name, None)


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
