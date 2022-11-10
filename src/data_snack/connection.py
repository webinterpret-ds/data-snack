from abc import ABCMeta, abstractmethod
from typing import Text, List, Dict


class Connection(ABCMeta):

    @abstractmethod
    def get(self, key: Text):
        ...

    @abstractmethod
    def set(self, key: Text, value: Text):
        ...

    @abstractmethod
    def mget(self, keys: List[Text]):
        ...

    @abstractmethod
    def mset(self, values: Dict[Text, Text]):
        ...
