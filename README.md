# Data Snack 

# About
Data Snack is a minimalistic framework for storing and accessing structured data.

It uses an `Entity` objects to define a schema for your data. `Snack` provides an interface
for automatically serializing and storing entities in a cache database of you choice. 
General interface that allows you to use different backends: redis, memcached.

## Features

- `Entity` objects are stored in a compress form to reduce memory usage.
- `Snack` is using `Entity` fields to define a unique key to represent an object stored in the db.
- `Snack` is supporting batch saving and reading data to achieve high performance.

## Core concepts
- `Entity` - a class defines a schema of single object stored in db
- `key fields` - a list of fields (defined as a list of `str` values)
  that will be used to create a key for a given `Entity` object.
- `key values` - a list of values for `key fields` from given `Entity`
- `key` - a `str` value created for a given Entity
    - created in a format: `<Entity type name>-<key value 1>_<key value 2>...<key value N>`

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
The first thing you need to do is to define an `Entity`.
Entities are used to define a common structure of the objects stores in your database.

We are recommending adding data validation to your entities. 
The easiest way is using `pydantic` for type validation of all entity fields.

```python
from pydantic.dataclasses import dataclass
from typing import Text
from data_snack.entities import Entity

@dataclass
class Person(Entity):
    index: Text
    name: Text
```

### 2. Connect to Redis
Connect to you a cache database of your choice.
In this example we are using `Redis`, but you could also use `Memcached` if you want.

```python
import redis
redis_connection = redis.Redis(host='127.0.0.1', port=6379, password='')
```

### 3. Create Snack instance
In this step we create a `Snack` instance and connect it to our `Redis` database.
Notice, that `Redis` client is wrapped in our `RedisConnection` class to ensure shared interface.
And at least we can register all entities that will be used in our project.
For each entity we specify a list of fields that will be used to define keys when saving our data.

```python
from data_snack import Snack
from data_snack.connections.redis import RedisConnection
snack = Snack(connection=RedisConnection(redis_connection))  # create instance
snack.register_entity(Person, key_fields=['index'])  # register your entity
```

### 4. Save and load your entities using Snack
You are ready to save and load data using `Snack`.

```python
snack.set(Person("1", "John"))
# 'Person-1'
entity = snack.get(Person, ["1"])
# Person(index='1', name='John')
snack.set_many([Person("1", "John"), Person("2", "Anna")])
# ['Person-1', 'Person-2']
entities = snack.get_many(Person, [["1"], ["2"]])
# [Person(index='1', name='John'), Person(index='2', name='Anna')]
```

### 4. Delete your entities using Snack
After you're done with your data you can delete it using `Snack`.

```python
snack.delete(Person, ["1"])
# Person(index='1', name='John')
snack.delete_many(Person, [["1"], ["2"]])
# [Person(index='1', name='John'), Person(index='2', name='Anna')]
```

# Documentation
## Access documentation
WIP. Documentation will be hosted on github pages.

## Setup documentation
Setup documentation directory
```bash
mkdir docs
cd docs
```
Create documentation scaffold. Make sure to select an option with separated directories for `source` and `build`.
```bash
sphinx-quickstart
```
Update `extensions` in `docs/source/conf.py`.
```python
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
```

## Update apidoc documentation
Before you start make sure to import project `src` directory at the very top of `docs/source/conf.py` file.
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))
```

Since documentation uses additional modules (other than base `data-snack`), we need to install additional requirements:
```bash
pip install -r docs/requirements.txt
```

Update the scaffold and generate the html docs.
```bash
sphinx-apidoc -o ./source ../src/data_snack
make html
```

# Contact
Plugin was created by the Data Science team from [Webinterpret](https://www.webinterpret.com/).

