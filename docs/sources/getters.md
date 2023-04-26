#


### getUserTable
[source](https://github.com/arnos-stuff/typer-tinydb\blob\master\typer_tinydb/utils.py\#L258)
```python
.getUserTable(
   table: str = ...
)
```

---
Returns the user table object for the given table name.


**Arguments**

table -- the name of the table to return


**Returns**

* when the user-defined DB can be found it returns a TinyDB object, else None is returned


----


### ugetKey
[source](https://github.com/arnos-stuff/typer-tinydb\blob\master\typer_tinydb/utils.py\#L279)
```python
.ugetKey(
   param: str, table: str
)
```

---
Function `ugetKey`. It takes two parameters, the `param` and the `table`. The `param` is the parameter that we want to search for in the table, and the `table` is the table that we want to search in.

The first thing that we do is check if the table is valid. If it is, we search for the param in the table. If the param is obfuscated, we deobfuscate it before searching. If we find the param, we return the key. If we don't find it, we return a 404 error.


**Args**

* **param** (str) : The parameter, or key, to be retrieved
* **table** (str) : The user-defined table from which it is retrieved.


----


### getKey
[source](https://github.com/arnos-stuff/typer-tinydb\blob\master\typer_tinydb/utils.py\#L340)
```python
.getKey(
   param: str
)
```

---
search for obfuscated params with matching deobfuscated values
or search for non-obfuscated params with matching values
return the results

----


### ugetValue
[source](https://github.com/arnos-stuff/typer-tinydb\blob\master\typer_tinydb/utils.py\#L307)
```python
.ugetValue(
   param: str, table: str, decode: bool = True
)
```


----


### getValue
[source](https://github.com/arnos-stuff/typer-tinydb\blob\master\typer_tinydb/utils.py\#L352)
```python
.getValue(
   param: str, decode: bool = True
)
```

---
The getValue function is used to get the deobfuscated value of the parameter. If there are multiple deobfuscated values, the first one is returned. If there is only one deobfuscated value, it is returned. If there are no deobfuscated values, an empty string is returned. The getKey function is used to get the parameter values, and then the deobfuscate_json function is used to deobfuscate the values.


**Args**

* **param** (str) : The name of the parameter to get the value of.
* **decode** (bool, optional) : Whether or not to deobfuscate the value. Defaults to True.


**Returns**

* **str**  : The deobfuscated value of the parameter.

