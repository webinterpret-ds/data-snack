# Data Snack 

# About
Data Snack is a minimalistic framework for storing and accessing structured data.

It uses an `Entity` objects to define a schema for your data. `Snack` provides an interface
for automatically serializing and storing entities in a cache database of you choice. 
General interface that allows you to use different backends: redis, memcached.

## Install
Data Snack can be easily installed using pypi repository.
```bash
pip install data_snack
```

# Usage
This examples shows a basic usage of defining an entity and using `Snack` to save and load it from the cache.
More examples can be found in the [Examples](examples/examples.md) section.

## Example 1 - Creating new entities and saving
### 1. Define entities
```python
from dataclasses import dataclass
from typing import Text
from data_snack.entities import Entity

@dataclass
class Person(Entity):
    index: Text
    name: Text
```

### 2. Connect to redis
```python
import redis
redis_connection = redis.Redis(host='127.0.0.1', port=6379, password='')
```

### 3. Create snack instance
```python
from data_snack import Snack
snack = Snack(connection=redis_connection)  # create instance
snack.register_entity(Person, keys=['index'])  # register your entity
```

### 4. Save and load your entities using Snack
```python
snack.set(Person("1", "John"))
# 'Person-1'
snack.get(Person, ["1"])
# Person(index='1', name='John')
snack.mset([Person("1", "John"), Person("2", "Anna")])
# ['Person-1', 'Person-2']
entities = snack.mget(CarEntity, [["1"], ["2"]])
# [Person(index='1', name='John'), Person(index='2', name='Anna')]
```

# Contact
Plugin was created by the Data Science team from [Webinterpret](https://www.webinterpret.com/).
