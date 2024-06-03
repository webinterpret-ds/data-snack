from typing import List, Dict


def map_values(mappings: Dict[str, str], values: List[str]) -> List[str]:
    return list(map(mappings.get, values))


def filter_missing_values(values: List[str]) -> List[str]:
    return list(filter(None, values))
