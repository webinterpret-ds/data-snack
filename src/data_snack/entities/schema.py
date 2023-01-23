from typing import Dict, Any, Callable, Type, get_type_hints

from pandas.core.dtypes.common import pandas_dtype

from data_snack.entities import Entity


EntitySchemaGetter = Callable[[Type[Entity], bool], Dict[str, Any]]


def _get_schema(func: Callable[[type], Any], entity_type: Type[Entity], exclude_fields: bool = False) -> Dict[str, Any]:
    schema = get_type_hints(entity_type)
    if exclude_fields:
        excluded_fields = entity_type.get_excluded_fields()
        return {k: func(v) for k, v in schema.items() if k not in excluded_fields}
    return {k: func(v) for k, v in schema.items()}


def get_entity_schema(entity_type: Type[Entity], exclude_fields: bool = False) -> Dict[str, Any]:
    """
    Gets `Entity` schema, i.e. {field: data type} mapping. Allows excluding Entities excluded fields.
    :param entity_type: Entity definition (class)
    :param exclude_fields: excludes Entity excluded fields if True
    :return: Entity schema
    """
    schema = _get_schema(func=lambda x: x, entity_type=entity_type, exclude_fields=exclude_fields)
    return schema


def get_entity_pandas_schema(entity_type: Type[Entity], exclude_fields: bool = False) -> Dict[str, Any]:
    """
    Gets `Entity` schema, i.e. {field: data type} mapping. Allows excluding Entities excluded fields. Returned schema
    is translated to `pandas` data types, e.g. int -> `dtype('int64')`.
    :param entity_type: Entity definition (class)
    :param exclude_fields: excludes Entity excluded fields if True
    :return: Entity schema with data types understood by pandas
    """
    schema = _get_schema(func=lambda x: pandas_dtype(x), entity_type=entity_type, exclude_fields=exclude_fields)
    return schema
