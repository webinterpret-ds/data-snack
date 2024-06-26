from typing import List, Optional

import pandas as pd
import pytest

from data_snack import DataFrameWrap, Snack
from data_snack.wrap.exceptions import DataFrameMissingKeyColumn
from tests.data_snack.conftest import Car


@pytest.fixture
def wrap_dataframe(snack: Snack) -> DataFrameWrap:
    """`DataFrameWrap` object created for the `Car` entity."""
    snack.register_entity(Car)
    return snack.create_wrap(Car, DataFrameWrap)


@pytest.fixture
def data_df(example_car_entities: List[Car]) -> pd.DataFrame:
    """Data frame containing all data: both keys and field values of the entity."""
    return pd.DataFrame(example_car_entities)


@pytest.fixture
def data_with_duplicates_df(example_car_entities_with_duplicates: List[Car]) -> pd.DataFrame:
    """
    Data frame containing all data: both keys and field values of the entity.
    Some entities are duplicated.
    """
    return pd.DataFrame(example_car_entities_with_duplicates)


@pytest.fixture
def data_with_none_df(index_df: pd.DataFrame, example_car_entities_none: List[Optional[Car]]) -> pd.DataFrame:
    """
    Data frame containing all data: both keys and field values of the entity.
    Since some entities were not available so None is returned.
    """
    return pd.merge(
        index_df,
        pd.DataFrame([row for row in example_car_entities_none if row]),
        on=Car.get_keys(),
        how="left"
    )


@pytest.fixture
def index_df(data_df: pd.DataFrame) -> pd.DataFrame:
    """Data frame containing only columns assigned as `keys` for given entity."""
    return pd.DataFrame([{"index": "1"}, {"index": "2"}])


@pytest.fixture
def index_with_duplicates_df(data_df: pd.DataFrame) -> pd.DataFrame:
    """Data frame containing only columns assigned as `keys` for given entity."""
    return pd.DataFrame([{"index": "1"}, {"index": "2"}, {"index": "1"}])


@pytest.fixture
def wrong_index_df(data_df: pd.DataFrame) -> pd.DataFrame:
    """Data frame containing only columns assigned as `keys` for given entity."""
    return pd.DataFrame([{"brand": "1"}, {"brand": "2"}])


def test_set_dataframe(
    wrap_dataframe: DataFrameWrap,
    data_df: pd.DataFrame,
    example_car_entities_hashes: List[bytes],
) -> None:
    """Testing saving a data frame containing entities data to the database."""
    expected_keys = ("Car-1-" + data_df["index"]).tolist()
    wrap_dataframe.snack.connection.connection.mset.return_value = expected_keys

    # keys are returned unmodified
    keys = wrap_dataframe.set_dataframe(data_df)
    assert keys == expected_keys

    # connection is called with a dict containing keys and hashed entities built based on the data frame values
    expected_payload = dict(zip(expected_keys, example_car_entities_hashes))
    wrap_dataframe.snack.connection.connection.mset.assert_called_with(expected_payload)


def test_get_dataframe(
    wrap_dataframe: DataFrameWrap,
    index_df: pd.DataFrame,
    data_df: pd.DataFrame,
    example_car_entities_hashes: List[bytes],
) -> None:
    """Testing reading a data frame with entities values based on a provided data frame with key columns."""
    wrap_dataframe.snack.connection.connection.mget.return_value = (
        example_car_entities_hashes
    )

    # returned data frame is created based on the compressed entities stored in the database
    df = wrap_dataframe.get_dataframe(index_df)
    assert df.equals(data_df)

    # connection is called with a list of entity keys
    expected_keys = ("Car-1-" + index_df["index"]).tolist()
    wrap_dataframe.snack.connection.connection.mget.assert_called_with(expected_keys)


def test_get_dataframe_data_with_none(
        wrap_dataframe: DataFrameWrap,
        index_df: pd.DataFrame,
        data_with_none_df: pd.DataFrame,
        example_car_entities_hashes_none: List[bytes],
) -> None:
    """Testing reading a data frame with entities values based on a provided data frame with key columns."""
    wrap_dataframe.snack.connection.connection.mget.return_value = (
        example_car_entities_hashes_none
    )

    # returned data frame is created based on the compressed entities stored in the database
    df = wrap_dataframe.get_dataframe(index_df)
    assert df.equals(data_with_none_df)

    # connection is called with a list of entity keys
    expected_keys = ("Car-1-" + index_df["index"]).tolist()
    wrap_dataframe.snack.connection.connection.mget.assert_called_with(expected_keys)


def test_get_dataframe_data_with_duplicates(
        wrap_dataframe: DataFrameWrap,
        index_with_duplicates_df: pd.DataFrame,
        data_with_duplicates_df: pd.DataFrame,
        example_car_entities_with_duplicates_hashes: List[bytes],
) -> None:
    """Testing reading a data frame with entities values based on a provided data frame with key columns."""
    wrap_dataframe.snack.connection.connection.mget.return_value = (
        example_car_entities_with_duplicates_hashes
    )

    # returned data frame is created based on the compressed entities stored in the database
    df = wrap_dataframe.get_dataframe(index_with_duplicates_df)
    assert df.equals(data_with_duplicates_df)

    # connection is called with a list of entity keys
    expected_keys = ("Car-1-" + index_with_duplicates_df["index"]).tolist()
    wrap_dataframe.snack.connection.connection.mget.assert_called_with(expected_keys)


def test_get_dataframe_missing_columns(
    wrap_dataframe: DataFrameWrap, wrong_index_df: pd.DataFrame
) -> None:
    """Testing reading a data frame, but the input data frame is missing required columns."""
    with pytest.raises(DataFrameMissingKeyColumn):
        wrap_dataframe.get_dataframe(wrong_index_df)
