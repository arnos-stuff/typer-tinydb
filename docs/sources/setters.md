#


### upsert_param
[source](https://github.com/arnos-stuff/typer-tinydb/blob/master/typer_tinydb/utils.py/#L189)
```python
.upsert_param(
   param: str, value: Any, obfuscate: bool = False
)
```

---
This function is used to upsert a parameter (param) and its corresponding value (value) to the global database.
The function takes in 3 parameters: param, value, and obfuscate. 
The param parameter is a string that contains the parameter name. 
The value parameter can take in any type of value, and it contains the value to be upserted to the database.
The obfuscate parameter is a boolean value that determines if the parameter and its corresponding value will be obfuscated before being stored in the database.
The function first creates a Query object called Param.
It then checks if the obfuscate parameter is set to True. If it is, then the param and value parameters are obfuscated before being stored in the database. 
If it is not, then the param and value parameters are not obfuscated before being stored in the database.
The function then upserts the param and value to the database, and also stores the timestamp, machine, and obfuscated parameters.

----


### upsert_param_udb
[source](https://github.com/arnos-stuff/typer-tinydb/blob/master/typer_tinydb/utils.py/#L321)
```python
.upsert_param_udb(
   table: TinyDB, param: str = ..., value: Any = ..., obfuscate: bool = False
)
```


----


### create_table
[source](https://github.com/arnos-stuff/typer-tinydb/blob/master/typer_tinydb/utils.py/#L218)
```python
.create_table(
   table: str = ..., schema: dict = None
)
```

---
Create a table with the given name and schema. If the table already exists, the schema is updated.
