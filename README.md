# A Typer config file get/set boilerplate

# A small note

The docs are generated using mkdocs and mike:

```python
pip install mkdocs mike mkdocs-material
```

besides the obvious `mkdocs build` and `mkdocs gh-deploy` you should use

```
mike deploy --push --update-aliases 0.1.2 latest
```
where `0.1.2` is some tag

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

## Command `typer-tinydb-config`

Configure the app 🛠️.

**Usage**:

```console
$ typer-tinydb-config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `get`: Get a config value.
* `list`: List all config values.
* `reset`: Reset all config values.
* `set`: Set a config value.

### Command `typer-tinydb-config get`

Get a config value.

**Usage**:

```console
$ typer-tinydb-config get [OPTIONS] PARAM
```

**Arguments**:

* `PARAM`: The parameter to get.  [required]

**Options**:

* `--help`: Show this message and exit.

### Command `typer-tinydb-config list`

List all config values.

**Usage**:

```console
$ typer-tinydb-config list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### Command `typer-tinydb-config reset`

Reset all config values.

**Usage**:

```console
$ typer-tinydb-config reset [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### Command `typer-tinydb-config set`

Set a config value.

**Usage**:

```console
$ typer-tinydb-config set [OPTIONS] PARAM VALUE
```

**Arguments**:

* `PARAM`: The parameter to set.  [required]
* `VALUE`: The value to set the parameter to.  [required]

**Options**:

* `--help`: Show this message and exit.


# Future updates

The idea is to add some extra features like

- [ ] Creating your own tables from the CLI
- [ ] Adding some customization (in terms of colors) for the printing
- [ ] Adding obfuscation so that your `.json` config file cannot be easily glanced at by bypassers

