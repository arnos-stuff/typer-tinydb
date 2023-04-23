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