# Data Snack 

# About

## Install
Plugin can be easily installed using pypi repository.
```bash
pip install data_snack
```

# Usage
## Example 1

### 1. Define entities
```python
from dataclasses import dataclass
from typing import Text
from data_snack.entities import Entity

@dataclass
class CarEntity(Entity):
    index: Text
    price: int
   brand: Text
```

### 2. Connect to redis
```python
import redis
redis_connection = redis.Redis(
   host='127.0.0.1',
   port=6379,
   password=''
)
```

### 3. Create snack instance
```python
from data_snack import Snack
snack = Snack(connection=redis_connection)  # create instance
snack.register_entity(CarEntity, keys=['index'])  # register your entity
```

### 4. Create test dataset 
```python
import pandas as pd
df = pd.DataFrame([
    {"index": "1", "brand": "Audi", "price": 17000},
    {"index": "2", "brand": "Opel", "price": 4000},
    {"index": "3", "brand": "Audi", "price": 7000},
    {"index": "4", "brand": "Toyota", "price": 14000},
])
data = [CarEntity(**v) for v in df.to_dict(orient="records")]
```


### 5. Save and load data
```python
snack.set(data[1])
# 'CarEntity-2'
snack.get(CarEntity, ["1"])
# CarEntity(index='1', price=17000, brand='Audi')
entities = snack.mget(CarEntity, [["1"], ["2"], ["3"]])
# [CarEntity(index='1', price=17000, brand='Audi'), CarEntity(index='2', price=4000, brand='Opel'), CarEntity(index='3', price=7000, brand='Audi')]
snack.mset(data)
# ['CarEntity-1', 'CarEntity-2', 'CarEntity-3', 'CarEntity-4']
```

# Contact
Plugin was created by the Data Science team from [Webinterpret](https://www.webinterpret.com/).
