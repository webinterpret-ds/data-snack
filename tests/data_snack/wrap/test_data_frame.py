from typing import List

import pandas as pd
import pytest

from data_snack import Snack, DataFrameWrap
from tests.data_snack.conftest import Car


@pytest.fixture
def wrap_dataframe(snack: Snack) -> DataFrameWrap:
    """`DataFrameWrap` object created for the `Car` entity."""
    snack.register_entity(Car, keys=['index'])
    return snack.create_wrap(Car, DataFrameWrap)


@pytest.fixture
def data_df(example_entities: List[Car]) -> pd.DataFrame:
    """`Data frame` containing all data: both keys and field values of the entity."""
    return pd.DataFrame(example_entities)


@pytest.fixture
def index_df(data_df: pd.DataFrame) -> pd.DataFrame:
    """Data frame containing only columns assigned as `keys` for given entity."""
    return data_df[['index']]


def test_set_dataframe(
        wrap_dataframe: DataFrameWrap, data_df: pd.DataFrame, example_entities_hashes: List[bytes]
) -> None:
    """Testing saving a data frame containing entities data to the database."""
    expected_keys = ("Car-"+data_df['index']).tolist()
    wrap_dataframe.snack.connection.connection.mset.return_value = expected_keys

    # keys are returned unmodified
    keys = wrap_dataframe.set_dataframe(data_df)
    assert keys == expected_keys

    # connection is called with a dict containing keys and hashed entities built based on the data frame values
    expected_payload = dict(zip(expected_keys, example_entities_hashes))
    wrap_dataframe.snack.connection.connection.mset.assert_called_with(expected_payload)


def test_get_dataframe(
        wrap_dataframe: DataFrameWrap,
        index_df: pd.DataFrame,
        data_df: pd.DataFrame,
        example_entities_hashes: List[bytes]
) -> None:
    """Testing reading a data frame with entities values based on a provided data frame with key columns."""
    wrap_dataframe.snack.connection.connection.mget.return_value = example_entities_hashes

    # returned data frame is created based on the compressed entities stored in the database
    df = wrap_dataframe.get_dataframe(index_df)
    assert df.equals(data_df)

    # connection is called with a list of entity keys
    expected_keys = ("Car-"+index_df['index']).tolist()
    wrap_dataframe.snack.connection.connection.mget.assert_called_with(expected_keys)
