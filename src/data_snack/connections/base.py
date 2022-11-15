from abc import ABC, abstractmethod
from typing import Text, List, Dict, Union


class Connection(ABC):

    @abstractmethod
    def get(self, key: Text):
        ...

    @abstractmethod
    def set(self, key: Text, value: Union[Text, bytes]):
        ...

    @abstractmethod
    def get_many(self, keys: List[Text]) -> Dict[Text, bytes]:
        ...

    @abstractmethod
    def set_many(self, values: Dict[Text, Union[Text, bytes]]):
        ...

    @abstractmethod
    def keys(self, pattern: Text) -> List[bytes]:
        ...
