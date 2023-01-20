from typing import Callable, List, Type, get_type_hints

from data_snack.entities import Entity


def _define_meta(cls: Type[Entity], keys: List[str], excluded_fields: List[str]) -> Type[Entity]:
    if cls.Meta.keys:
        raise ValueError(f"{cls.__name__}.Meta has been set already.")
    elif wrong_fields := [x for x in keys + excluded_fields if x not in list(get_type_hints(cls))]:
        raise LookupError(f"{wrong_fields} not found in '{cls.__name__}' class fields.")
    else:
        cls.Meta = type("Meta", (object,), {"keys": keys, "excluded_fields": excluded_fields})
    return cls


def set_entity_meta(
    cls: Type[Entity] = None, /, *, keys: List[str], excluded_fields: List[str] = None
) -> Callable[[Type[Entity]], Type[Entity]]:
    """
    Sets `Meta` for `Entity`. Once set Meta can not be set again. `Meta` is set if at least its `keys` is a non empty
    list. It is possible to call it as a function on predefined Entity class, then `cls` argument has to be provided.
    :param cls: class for which `Meta` is set
    :param keys: desired `Entity.Meta.keys`
    :param excluded_fields: desired `Entity.Meta.excluded_fields`
    :return: Entity with well defined Meta
    """
    if excluded_fields is None:
        excluded_fields = []

    def wrap(cls: Type[Entity]) -> Type[Entity]:
        return _define_meta(cls=cls, keys=keys, excluded_fields=excluded_fields)

    # standard usage as a decorator
    if cls is None:
        return wrap

    # usage as a function
    return wrap(cls)
