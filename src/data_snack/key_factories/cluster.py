from dataclasses import dataclass
from typing import Text

from data_snack.key_factories.base import KeyFactory


@dataclass
class ClusterKeyFactory(KeyFactory):
    def get_key(self, type_name: Text, *key_values: Text) -> Text:
        return f"{{{type_name}}}-{'_'.join(map(str, key_values))}"

    def get_pattern(self, type_name: Text) -> Text:
        return f"{{{type_name}}}-*"
