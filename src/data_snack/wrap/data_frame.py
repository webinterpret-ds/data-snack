from dataclasses import asdict, dataclass
from typing import List, Text

import pandas as pd

from data_snack.wrap import EntityWrap
from data_snack.wrap.exceptions import DataFrameMissingKeyColumn


@dataclass
class DataFrameWrap(EntityWrap):
    def set_dataframe(self, df: pd.DataFrame) -> List[Text]:
        """
        Uses a data frame as a source for creating multiple Entity objects.
        Data frame needs to follow the schema defined by the Entity.
        Each row in the data frame defines a single Entity that will be saved in the db.

        :param df: a data frame with entities in a tabular form
        :return: a list of keys created for entities
        """
        # TODO: Add fields validation for df
        data = [self.entity_type(**v) for v in df.to_dict(orient="records")]
        return self.set_many(data)

    def get_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Uses a data frame to retrieve data from the db.
        Input data frame should contain all the columns corresponding
        to keys of selected Entity type.

        :param df: a data frame containing columns with entity keys
        :return: a full data frame containing all retrieved entities
        """
        required_key_columns = self.entity_type.get_keys()
        if missing_columns := set(required_key_columns) - set(df.columns):
            raise DataFrameMissingKeyColumn(
                f"Provided data frame is missing columns: {missing_columns}"
            )

        data = self.get_many(df[required_key_columns].values.tolist())
        output_df = pd.DataFrame(
            [row for row in data if row],
            columns=self.entity_type.get_all_fields()
        )

        return pd.merge(
            df,
            output_df.drop_duplicates(subset=required_key_columns),
            on=required_key_columns,
            how='left'
        )
