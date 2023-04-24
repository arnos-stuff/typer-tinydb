
[![PyPI version](https://badge.fury.io/py/typer-tinydb.svg)](https://badge.fury.io/py/typer-tinydb) [![GitHub License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://raw.githubusercontent.com/arnos-stuff/typer-tinydb/master/LICENSE)
[![codecov](https://codecov.io/gh/arnos-stuff/typer-tinydb/branch/master/graph/badge.svg?token=7MP5WBU8GI)](https://codecov.io/gh/arnos-stuff/typer-tinydb)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/arnos-stuff/typer-tinydb/tree/master.svg?style=shield "CircleCI Build Status")](https://dl.circleci.com/status-badge/redirect/gh/arnos-stuff/typer-tinydb/tree/master)

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
super-app cfg set some-key '20-hS407zuqYKQ8tPP2r5'
```

You can obviously use `super-app config get` and others, or any name you attribute to it.

## Using it within python modules

The CLI key-values are stored in a tinydb instance that is available by just importing the table named `globals`:

```python
from typer_tinydb import db, globals, where
```

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

Go check out the [documentation page 🚀](https://arnos-stuff.github.io/typer-tinydb)