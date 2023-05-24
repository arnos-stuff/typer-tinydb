
[![PyPI version](https://badge.fury.io/py/typer-tinydb.svg)](https://badge.fury.io/py/typer-tinydb) [![GitHub License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://raw.githubusercontent.com/arnos-stuff/typer-tinydb/master/LICENSE)
[![codecov](https://codecov.io/gh/arnos-stuff/typer-tinydb/branch/master/graph/badge.svg?token=7MP5WBU8GI)](https://codecov.io/gh/arnos-stuff/typer-tinydb)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/arnos-stuff/typer-tinydb/tree/master.svg?style=shield "CircleCI Build Status")](https://dl.circleci.com/status-badge/redirect/gh/arnos-stuff/typer-tinydb/tree/master)
[![PyPI dls](https://img.shields.io/pypi/dm/typer-tinydb?color=teal&logo=python&logoColor=green)](https://pypi.org/project/typer-tinydb/)


# A Typer config file get/set boilerplate

# Using the boilerplate

## Aliases and subcommands

We recommand the following aliases, which are readily available out of the box.

- `config`
- `cfg`
- `c`

This way, if your app is named `super-app`

And is defined in `super_app.py` roughly as follows:

```python

import typer

# ... some imports

app = typer.Typer(
    name='super-app',
    # ... other args
)
```

You just have to add the following below:

```python
from typer_tinydb import cfg, config # those are typer apps

app.add_typer(cfg) # the cfg app
app.add_typer(config) # the config app
```

You can rename them however you like by using

```python
app.add_typer(cfg, name='my-super-config')
```

## Using it on the command line

With the same configuration as above, your new app can now run the commands:

```bash
super-app cfg list # list config key:value pairs
super-app cfg get some-key # get the values linked to the key 'some-key'
super-app cfg set some-key '20-hS407zuqYKQ8tPP2r5' # store some hash or token into your settings file
super-app cfg set -k user23 'supersecretpassword' # it's going to get obfuscated so looking at the JSON doesn't help
```

You can obviously use `super-app config get` and others, or any name you attribute to it.

## Using it within python modules

The CLI key-values are stored in a tinydb instance that is available by just importing the table named `globals`:

```python
from typer_tinydb import db, globals, where
```

### Insert / Upsert

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

### Get Keys / Values

There are two pre-made functions: `getKey` and `getValue`. The key difference is as follows:

* `getKey` returns **all the values associated with key `key`**
* `getValue` arbitrarily returns the first encountered value.

# The underlying database

You can create any table using the database object `db`, please [check out the tinydb docs !](https://tinydb.readthedocs.io/)

To get the key just use `where` :

```python
returns = globals.search(where('param') == param)
```

To insert new values or update existing, use the `upsert` function:

```python
Param = Query()

globals.upsert({
    "param": param,
    "value": value,
    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "machine": socket.gethostname(),
    },
    Param.param == param
)
```
# Commands

Go check out the [commands page 🚀](commands.md)