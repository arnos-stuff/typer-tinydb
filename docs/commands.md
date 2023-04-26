---
tags:
    - cli
    - typer
    - tinydb
    - docs

---

# Command line options and commands

## Command `config`

Configure the app 🛠️.

**Usage**:

```console
$ config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `+`: Set a config value.
* `++`: Set a config value within a user-defined...
* `+T`: Creates a new table.
* `?`: Get a config value.
* `??`: Get a config value from a user-defined table.
* `create-table`: Creates a new table.
* `crtab`: Creates a new table.
* `drop-table`: Removes a user-defined table.
* `dropt`: Removes a user-defined.
* `get`: Get a config value.
* `list`: List all config values.
* `ls`: List all config values.
* `reset`: Reset all config values.
* `set`: Set a config value.
* `test`: Run tests 🧪.
* `uget`: Get a config value from a user-defined table.
* `uset`: Set a config value within a user-defined...

### Command `config +`

Set a config value. Alias for `set`

**Usage**:

```console
$ config + [OPTIONS] PARAM VALUE
```

**Arguments**:

* `PARAM`: The parameter to set.  [required]
* `VALUE`: The value to set the parameter to.  [required]

**Options**:

* `-k, --obfuscate`: Whether to make the key and param impossible to read without postprocessing. Not a replacement for cryptography, but makes it safer.
* `--help`: Show this message and exit.

### Command `config ++`

Set a config value within a user-defined table. Alias for `uset`

**Usage**:

```console
$ config ++ [OPTIONS] TABLE PARAM VALUE
```

**Arguments**:

* `TABLE`: The user-defined table to populate with this new key-value pair.  [required]
* `PARAM`: The parameter to set.  [required]
* `VALUE`: The value to set the parameter to.  [required]

**Options**:

* `-k, --obfuscate`: Whether to make the key and param impossible to read without postprocessing. Not a replacement for cryptography, but makes it safer.
* `--help`: Show this message and exit.

### Command `config +T`

Creates a new table. Alias for `create-table`

**Usage**:

```console
$ config +T [OPTIONS] TABLE
```

**Arguments**:

* `TABLE`: The name of the table to create.  [required]

**Options**:

* `--schema TEXT`: Not yet supported.
* `--help`: Show this message and exit.

### Command `config ?`

Get a config value. Alias for `get`

**Usage**:

```console
$ config ? [OPTIONS] PARAM
```

**Arguments**:

* `PARAM`: The parameter to get.  [required]

**Options**:

* `--help`: Show this message and exit.

### Command `config ??`

Get a config value from a user-defined table. Alias for `uget`

**Usage**:

```console
$ config ?? [OPTIONS] TABLE [PARAM]
```

**Arguments**:

* `TABLE`: The user-defined table to fetch the variable from.  [required]
* `[PARAM]`: The parameter to get. Either use `all` or a specififc param

**Options**:

* `--help`: Show this message and exit.

### Command `config create-table`

Creates a new table.

**Usage**:

```console
$ config create-table [OPTIONS] TABLE
```

**Arguments**:

* `TABLE`: The name of the table to create.  [required]

**Options**:

* `--schema TEXT`: Not yet supported.
* `--help`: Show this message and exit.

### Command `config crtab`

Creates a new table. Alias for `create-table`

**Usage**:

```console
$ config crtab [OPTIONS] TABLE
```

**Arguments**:

* `TABLE`: The name of the table to create.  [required]

**Options**:

* `--schema TEXT`: Not yet supported.
* `--help`: Show this message and exit.

### Command `config drop-table`

Removes a user-defined table.

**Usage**:

```console
$ config drop-table [OPTIONS] TABLE
```

**Arguments**:

* `TABLE`: The name of the table to drop.  [required]

**Options**:

* `-s, --schema TEXT`: Not yet supported.
* `-w, --wipe`: Whether to remove all the data from disk, cannot be undone.
* `--help`: Show this message and exit.

### Command `config dropt`

Removes a user-defined. Alias for `drop-table`

**Usage**:

```console
$ config dropt [OPTIONS] TABLE
```

**Arguments**:

* `TABLE`: The name of the table to drop.  [required]

**Options**:

* `-s, --schema TEXT`: Not yet supported.
* `-w, --wipe`: Whether to remove all the data from disk, cannot be undone.
* `--help`: Show this message and exit.

### Command `config get`

Get a config value.

**Usage**:

```console
$ config get [OPTIONS] PARAM
```

**Arguments**:

* `PARAM`: The parameter to get.  [required]

**Options**:

* `--help`: Show this message and exit.

### Command `config list`

List all config values.

**Usage**:

```console
$ config list [OPTIONS]
```

**Options**:

* `-k, --decode`: Whether to list the obfuscated key/value pairs in clear text
* `-t, --table TEXT`: Whether to list the contents of a specififc user-defined table
* `-a, --all`: Whether to list all the uer defined tables aswell. Might be very slow.
* `--help`: Show this message and exit.

### Command `config ls`

List all config values. Alias for `list`

**Usage**:

```console
$ config ls [OPTIONS]
```

**Options**:

* `-k, --decode`: Whether to list the obfuscated key/value pairs in clear text
* `-t, --table TEXT`: Whether to list the contents of a specififc user-defined table
* `-a, --all`: Whether to list all the uer defined tables aswell. Might be very slow.
* `--help`: Show this message and exit.

### Command `config reset`

Reset all config values.

**Usage**:

```console
$ config reset [OPTIONS]
```

**Options**:

* `-t, --table TEXT`: Whether to list the contents of a specififc user-defined table
* `-a, --all`: Whether to reset all the uer defined tables aswell. Might be very slow.
* `-f, --file`: Whether to remove the entire file.
* `--help`: Show this message and exit.

### Command `config set`

Set a config value.

**Usage**:

```console
$ config set [OPTIONS] PARAM VALUE
```

**Arguments**:

* `PARAM`: The parameter to set.  [required]
* `VALUE`: The value to set the parameter to.  [required]

**Options**:

* `-k, --obfuscate`: Whether to make the key and param impossible to read without postprocessing. Not a replacement for cryptography, but makes it safer.
* `--help`: Show this message and exit.

### Command `config test`

Run tests 🧪.

**Usage**:

```console
$ config test [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### Command `config uget`

Get a config value from a user-defined table.

**Usage**:

```console
$ config uget [OPTIONS] TABLE [PARAM]
```

**Arguments**:

* `TABLE`: The user-defined table to fetch the variable from.  [required]
* `[PARAM]`: The parameter to get. Either use `all` or a specififc param

**Options**:

* `--help`: Show this message and exit.

### Command `config uset`

Set a config value within a user-defined table.

**Usage**:

```console
$ config uset [OPTIONS] TABLE PARAM VALUE
```

**Arguments**:

* `TABLE`: The user-defined table to populate with this new key-value pair.  [required]
* `PARAM`: The parameter to set.  [required]
* `VALUE`: The value to set the parameter to.  [required]

**Options**:

* `-k, --obfuscate`: Whether to make the key and param impossible to read without postprocessing. Not a replacement for cryptography, but makes it safer.
* `--help`: Show this message and exit.
