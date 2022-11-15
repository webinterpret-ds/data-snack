from typing import List, Text

import pandas as pd

from ..snack import EntityWrap


def set_dataframe(wrap: EntityWrap, df: pd.DataFrame) -> List[Text]:
    data = [wrap.entity_type(**v) for v in df.to_dict(orient="records")]
    return wrap.set_many(data)


def get_dataframe(wrap: EntityWrap, df: pd.DataFrame) -> pd.DataFrame:
    keys = wrap.snack.registry[wrap.entity_type_name].keys
    data = wrap.get_many(df[keys].values.tolist())
    return pd.DataFrame(data)
