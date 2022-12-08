********
Examples
********
In this section we will go through a few examples of how ``Snack`` can be used to save and retrieve your entities from the database.

Example 1 - Creating new entities and saving
############################################
This is a basic example explaining how to define new, save and retrieve your entity using ``Snack``.

1. Define entities
******************
The first thing you need to do is to define an ``Entity``. Entities are used to define a common structure of the objects stores in your database.
They provide a schema for fields and their types. The schema is used to validate the data whenever you are trying to save it.

We recommend adding additional layer of validation using ``dataclass`` type validation. For example through using ``pydantic.dataclass`` decorator.

.. code-block:: python

	from pydantic.dataclasses import dataclass
	from typing import Text
	from data_snack.entities import Entity

	@dataclass
	class Car(Entity):
		index: Text
		price: int
		brand: Text

2. Connect to redis
*******************
In these examples we are using ``Redis`` as a backend for our data. But you could easily adjust it to your needs as long as your client will follow
the interface defined by ``data_snack.connection.Connection`` class.

.. code-block:: python

	import redis
	redis_connection = redis.Redis(
	   host='127.0.0.1',
	   port=6379,
	   password=''
	)

3. Create snack instance
************************
To start you need to create a ``Snack`` client using the connection created in the previous step. Then, you need to register all entities you will use.
While registering the entity you will also select which columns will be used as keys.

.. code-block:: python

	from data_snack import Snack
	snack = Snack(connection=redis_connection)  # create instance
	snack.register_entity(Car, keys=['index'])  # register your entity

4. Save and load single entity
******************************
You can now use ``Snack`` to save and load your entities. Notice, that since the entity keys are defined as a list, when getting the entity you need to provide keys are a list.

.. code-block:: python

	snack.set(Car(index="1", brand="Audi", price=17000))
	# 'Car-2'
	snack.get(Car, ["1"])
	# Car(index='1', price=17000, brand='Audi')

5. Save and load multiple entities
**********************************
You can also use `mset` and `mget` to save and load multiple objects. This function is using an optimized way for handling multiple entities. So this way will be always faster than doing it manually using the standard `get` and `set`.

.. code-block:: python

	data = [
		Car(index="1", brand="Audi", price=17000),
		Car(index="2", brand="Opel", price=4000),
		Car(index="3", brand="Audi", price=7000),
		Car(index="4", brand="Toyota", price=14000),
	]

	snack.set_many(data)
	# ['Car-1', 'Car-2', 'Car-3', 'Car-4']
	entities = snack.get_many(Car, [["1"], ["2"], ["3"], ["4"]])
	# [Car(index='1', price=17000, brand='Audi'), Car(index='2', price=4000, brand='Opel'), Car(index='3', price=7000, brand='Audi')]

Example 2 - Using an EntityWrap
###############################
``EntityWrap`` are providing an easier interface for working with one selected type of entities.
This way you can access ``Snack`` without a need to specify the ``EntityType`` in each command.

.. code-block:: python

	car_wrap = snack.create_wrap(Car)
	car_wrap.set(Car(index="1", brand="Audi", price=17000))
	# 'Car-2'
	car_wrap.get(["1"])
	# Car(index='1', price=17000, brand='Audi')

Example 3 - Using data frame utils functions
############################################
In this example we will go through ``DataFrameWrap`` that was created to make working with ``pandas`` data frames easier.

1. Define your dataset
**********************
.. code-block:: python

	import pandas as pd
	df = pd.DataFrame([
		{"index": "1", "brand": "Audi", "price": 17000},
		{"index": "2", "brand": "Opel", "price": 4000},
		{"index": "3", "brand": "Audi", "price": 7000},
		{"index": "4", "brand": "Toyota", "price": 14000},
	])

2. Save and load you data frame
*******************************
You can save it by manually mapping the data frame into a list of python objects:

.. code-block:: python

	data = [Car(**v) for v in df.to_dict(orient="records")]

Or you can use a predefined helper function that will do that for you.
Function ``set_dataframe`` and ``get_dataframe`` provides an interface that allows you to save and load data frames object
that follows the schema defined by your entity.

.. code-block:: python

	df_wrap = snack.create_wrap(Car, DataFrameWrap)

	db_wrap.set_dataframe(df)
	# ['Car-1', 'Car-2', 'Car-3', 'Car-4']
	db_wrap.get_dataframe(df[['index']])

Notice, ``get_dataframe`` requires a data frame with columns defined as keys for given entity. As a result the function
will return all entities mapped into a data frame. It will not extend an input data frame,
but instead return a new one only with the fields defined by the selected ``Entity``.
