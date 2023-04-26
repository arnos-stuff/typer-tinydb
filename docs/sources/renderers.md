#


### renderQuery
[source](https://github.com/arnos-stuff/typer-tinydb\blob\master\typer_tinydb/utils.py\#L53)
```python
.renderQuery(
   results: List[Dict[str, Any]], large_columns: List[str] = None,
   first: str = 'param', last: str = 'value', decode: bool = True
)
```

---
Renders a TinyDB Query into a Rich Table


**Args**

* **results** (List[Dict[str,Any]]) : Results of a TinyDB Query, in the form of a list of dicts.
* **large_columns** (List[str], optional) : List of columns which should be given more width, 20% of terminal to be exact. Defaults to None.
* **first** (str, optional) : The first column to display in the table. Defaults to 'param'.
* **last** (str, optional) : The last column to display in the table. Defaults to 'value'.


**Raises**

* **ValueError**  : If the results do not correspond to tinydb-like query output, raises ValueError


**Returns**

* **Table**  : A rich renderable with the 


----


### tabCallback
[source](https://github.com/arnos-stuff/typer-tinydb\blob\master\typer_tinydb/utils.py\#L162)
```python
.tabCallback(
   table: TinyDB = ..., msg: str = ...
)
```


----


### renderAllTables
[source](https://github.com/arnos-stuff/typer-tinydb\blob\master\typer_tinydb/utils.py\#L173)
```python
.renderAllTables()
```

