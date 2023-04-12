from typing import Any, Callable, Dict, Type, get_type_hints

from data_snack.entities import Entity

EntitySchemaGetter = Callable[[Type[Entity], bool], Dict[str, Any]]


def get_entity_schema(
    entity_type: Type[Entity], exclude_fields: bool = False
) -> Dict[str, Any]:
    """
    Gets `Entity` schema, i.e. {field: data type} mapping. Allows excluding Entities excluded fields.
    :param entity_type: Entity definition (class)
    :param exclude_fields: excludes Entity excluded fields if True
    :return: Entity schema
    """
    schema = get_type_hints(entity_type)
    if exclude_fields:
        excluded_fields = entity_type.get_excluded_fields()
        return {k: v for k, v in schema.items() if k not in excluded_fields}
    return schema
