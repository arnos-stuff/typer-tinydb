---
tags:
    - python
    - lib
    - database
    - tinydb

---

# Functions to directly interact with the database

## Insert / Upsert

To insert a new value, the easiest is to use the `upsert_param`.

```python
def upsert_param(param:str, value:Any, obfuscate: bool = False):
    ...
```

This function is used to upsert a parameter (`param`) and its corresponding value (`value`) to the global database.
The function takes in 3 parameters: `param`, `value`, and `obfuscate`. 

* The `param` parameter is a string that contains the parameter name. 
* The `value` parameter can take in any type of value, and it contains the value to be upserted to the database.
* The `obfuscate` parameter is a boolean value that determines if the parameter and its corresponding value will be obfuscated before being stored in the database.

The function uses the usual `Query()` and `db.search(..)` from [tinydb](https://tinydb.readthedocs.io).

The function upserts the `param` and `value` to the database, and also stores the `timestamp`, `machine`, and a boolean to indicate wether parameters are obfuscated.

## Get Keys / Values

There are two pre-made functions: `getKey` and `getValue`. The key difference is as follows:

* `getKey` returns **all the values associated with key `key`**
* `getValue` arbitrarily returns the first encountered value.