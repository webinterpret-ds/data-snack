from dataclasses import dataclass
from typing import List, Text

import pandas as pd

from data_snack.wrap import EntityWrap


@dataclass
class DataFrameWrap(EntityWrap):
    def set_dataframe(self, df: pd.DataFrame) -> List[Text]:
        """

        :param df:
        :return:
        """
        data = [self.entity_type(**v) for v in df.to_dict(orient="records")]
        return self.set_many(data)

    def get_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """

        :param df:
        :return:
        """
        keys = self.snack.registry[self.entity_type_name].keys
        data = self.get_many(df[keys].values.tolist())
        return pd.DataFrame(data)
