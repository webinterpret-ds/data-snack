from data_snack.entities import EntityRegistry


def test_create_entity_registry(entity_registry: EntityRegistry):
    """Testing if constructor for the `EntityRegistry` objects works correctly."""
    assert type(entity_registry) is EntityRegistry
