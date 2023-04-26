
import typer

from .utils import (
    static, absolute_config, base64, configFile,
    console, current, cycle, db, deobfuscate_json,
    Any, Dict, getKey, getValue, globals, obfuscate_json,
    Path, renderQuery, upsert_param, TinyDB, Query, where,
    Table, rich, create_table, drop_table, getUserTable,
    datetime, ugetKey, ugetValue, upsert_param_udb, _tables,
    renderAllTables
)

__all__ = [
    "main", "cfg"
]


app = typer.Typer(
    name='config',
    help='Configure the app 🛠️.',
    hidden=False,
    add_completion=True,
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode='rich',
    )

cfg = typer.Typer(
    name='cfg',
    help='Configure the app 🛠️. Alias for `config`',
    add_completion=True,
    hidden=True,
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode='rich',
    )

@cfg.command(name='+', help='Set a config value. Alias for `set`', no_args_is_help=True, hidden=True)
@app.command(name='+', help='Set a config value. Alias for `set`', no_args_is_help=True, hidden=True)
@cfg.command(name='set', help='Set a config value.', no_args_is_help=True)
@app.command(name='set', help='Set a config value.', no_args_is_help=True)
def setter(
    param: str = typer.Argument(..., help = 'The parameter to set.'),
    value: str = typer.Argument(..., help='The value to set the parameter to.'),
    obfuscate: bool = typer.Option(
        False, '-k', '--obfuscate',
        help='Whether to make the key and param impossible to read without postprocessing. Not a replacement for cryptography, but makes it safer.')
    ):
    """Set a config value. These values are saved in the config tiny database.
    """
    upsert_param(param=param, value=value, obfuscate=obfuscate)
    obf_fmt = f"[red]{obfuscate}[/red]" if not obfuscate else f"[green]{obfuscate}[/green]"
    console.print(f'[bold green]✅ Set {param} to {value}[/] [dim][magenta](obfuscate=[/magenta]{obf_fmt})[/dim]')

@cfg.command(name='?', help='Get a config value. Alias for `get`', no_args_is_help=True, hidden=True)
@app.command(name='?', help='Get a config value. Alias for `get`', no_args_is_help=True, hidden=True)
@cfg.command(name='get', help='Get a config value.', no_args_is_help=True)
@app.command(name='get', help='Get a config value.', no_args_is_help=True)
def getter(
    param: str = typer.Argument(..., help='The parameter to get.'),
    ):
    """Get a config value. These values are saved in the config tiny database.
    """
    if param.lower() == 'all':
        lister()
        return typer.Exit(0)
    elif param.lower() == 'path':
        console.print(configFile.resolve())
        return typer.Exit(0)
    else:
        returns = getKey(param)
        if len(returns):
            table = renderQuery(results=returns)
            if table:
                console.print(table)
            else:
                console.print(f'[bold red]❌ {param} not found[/]')
        else:
            console.print(f'[bold red]❌ {param} not found[/]')


@cfg.command(name='ls', help='List all config values. Alias for `list`')
@app.command(name='ls', help='List all config values. Alias for `list`')
@cfg.command(name='list', help='List all config values.')
@app.command(name='list', help='List all config values.')
def lister(
        decode: bool = typer.Option(False,'-k', '--decode', help='Whether to list the obfuscated key/value pairs in clear text'),
        table: str = typer.Option(None, '-t', '--table', help='Whether to list the contents of a specififc user-defined table'),
        all: bool = typer.Option(False, '-a', '--all', help="Whether to list all the uer defined tables aswell. Might be very slow.")
    ):
    """List all config values. These values are saved in the config tiny database.
    """
    if all:
        renderAllTables()
        return
    elif table:
        tdb = getUserTable(table.lower().strip())
        if tdb is not None:
            rows = tdb.all()
        else:
            console.print(f"[dim blue]🕵️‍♀️ Seems user-defined file '{table}' is empty[/]")
            return
    else:
        rows = globals.all()
    tabr = renderQuery(results=rows, decode = decode)

    if not tabr:
        console.print(f'[dim blue]🕵️‍♀️ Seems your settings file is empty[/]')
    else:
        console.print(tabr)
    
@cfg.command(name='reset', help='Reset all config values.')
@app.command(name='reset', help='Reset all config values.')
def reset(
    table: str = typer.Option(None, '-t', '--table', help='Whether to list the contents of a specififc user-defined table'),
    all: bool = typer.Option(False, '-a', '--all', help="Whether to reset all the uer defined tables aswell. Might be very slow."),
    file: bool = typer.Option(False, '-f', '--file', help="Whether to remove the entire file.")
    ):
    """Reset all config values. These values are saved in the config tiny database.
    """
    if all:
        globals.truncate()
        for tab in map(lambda t: t['name'], _tables.all()):
            tabl = db.table(tab)
            tabl.truncate()
        console.print(f'[dim green] ✅ reset done [/]')
    elif table:
        target = _tables.get( where('name') == table.lower().strip())
        tgtdb = db.table(target['name']).truncate() if target else console.print(f'[dim yellow] 🌞 nothing to reset here [/]')
        console.print(f'[dim green] ✅ reset done [/]') if target else None
    elif file:
        configFile.unlink()
        for tn in _tables.all():
            db.table(tn['name']).drop()
    else:
        console.print(f'[dim yellow] 🌞 nothing to reset here [/]')
        
@cfg.command(name='test', help='Run tests 🧪.')
@app.command(name='test', help='Run tests 🧪.')
def test_runs():
    """Reset all config values. These values are saved in the config tiny database.
    """
    import pytest
    retcode = pytest.main(["--cov=./", "--cov-report=xml"])
    

@cfg.command(name='+T', help='Creates a new table. Alias for `create-table', no_args_is_help=True, hidden=True)
@app.command(name='+T', help='Creates a new table. Alias for `create-table`', no_args_is_help=True, hidden=True)    
@cfg.command(name='crtab', help='Creates a new table. Alias for `create-table`', no_args_is_help=True)    
@cfg.command(name='create-table', help='Creates a new table.', no_args_is_help=True)
@app.command(name='crtab', help='Creates a new table. Alias for `create-table`', no_args_is_help=True)
@app.command(name='create-table', help='Creates a new table.', no_args_is_help=True)
def create_tbl(
        table: str = typer.Argument(..., help="The name of the table to create."),
        schema: str = typer.Option(None, help="Not yet supported.")
    ):
    """Reset all config values. These values are saved in the config tiny database.
    """
    create_table(table=table)
    
@cfg.command(name='dropt', help='Removes a user-defined. Alias for `drop-table`', no_args_is_help=True)    
@cfg.command(name='drop-table', help='Removes a user-defined.', no_args_is_help=True)
@app.command(name='dropt', help='Removes a user-defined. Alias for `drop-table`', no_args_is_help=True)
@app.command(name='drop-table', help='Removes a user-defined table.', no_args_is_help=True)
def drop_tbl(
        table: str = typer.Argument(..., help="The name of the table to drop."),
        schema: str = typer.Option(None, '-s', '--schema', help="Not yet supported."),
        wipe: bool = typer.Option(False, '-w', '--wipe', help="Whether to remove all the data from disk, cannot be undone.")
    ):
    """Reset all config values. These values are saved in the config tiny database.
    """
    drop_table(table=table, rm=wipe)
    
@cfg.command(name='++', help='Set a config value within a user-defined table. Alias for `uset`', no_args_is_help=True, hidden=True)
@app.command(name='++', help='Set a config value within a user-defined table. Alias for `uset`', no_args_is_help=True, hidden=True)
@cfg.command(name='uset', help='Set a config value within a user-defined table.', no_args_is_help=True)
@app.command(name='uset', help='Set a config value within a user-defined table.', no_args_is_help=True)
def usetter(
    table: str = typer.Argument(..., help = 'The user-defined table to populate with this new key-value pair.'),
    param: str = typer.Argument(..., help = 'The parameter to set.'),
    value: str = typer.Argument(..., help='The value to set the parameter to.'),
    obfuscate: bool = typer.Option(
        False, '-k', '--obfuscate',
        help='Whether to make the key and param impossible to read without postprocessing. Not a replacement for cryptography, but makes it safer.')
    ):
    """Set a config value. These values are saved in the config tiny database.
    """
    try:
        udb = getUserTable(table=table)
    except ValueError:
        console.print(f"[bold red]❌ Table '{table}' not found[/]")
        typer.Exit(1)
        
    
    upsert_param_udb(udb, param=param, value=value, obfuscate=obfuscate)
    obf_fmt = f"[red]{obfuscate}[/red]" if not obfuscate else f"[green]{obfuscate}[/green]"
    console.print(f'[bold green]✅ Set {param} to {value}[/] in user-defined table [yellow] {table}[/yellow] [dim][magenta](obfuscate=[/magenta]{obf_fmt})[/dim]')
    

@cfg.command(name='??', help='Get a config value from a user-defined table. Alias for `uget`', no_args_is_help=True)
@app.command(name='??', help='Get a config value from a user-defined table. Alias for `uget`', no_args_is_help=True)
@cfg.command(name='uget', help='Get a config value from a user-defined table.', no_args_is_help=True)
@app.command(name='uget', help='Get a config value from a user-defined table.', no_args_is_help=True)
def getter(
    table: str = typer.Argument(..., help='The user-defined table to fetch the variable from.'),
    param: str = typer.Argument(None, help='The parameter to get. Either use `all` or a specififc param'),
    ):
    """Get a config value. These values are saved in the config tiny database.
    """
    if not param or param.lower() == 'all':
        if set(table) == {'?'}:
            lister(all=True)
            return typer.Exit(0)
        else:
            tdb = db.table(table.lower().strip())
            rtab = renderQuery(tdb.all())
            if rtab:
                console.print(rtab)
            else:
                console.print(f'[dim blue]🕵️‍♀️ Seems your user-defined table is empty[/]')
            return typer.Exit(0)
    elif param and param.lower() == 'path':
        console.print(configFile.resolve())
        return typer.Exit(0)
    else:
        returns = ugetKey(param, table=table)
        if returns == 404:
           console.print(f"[bold red]❌ Table '{table}' not found[/]")
        elif returns == 403:
            console.print(f'[bold green] ✅ Table found [/bold green] | [bold red]❌ {param} not found[/] in user-defined table [yellow] {table}[/yellow]')
        elif len(returns):
            ptable = renderQuery(results=returns)
            if ptable:
                console.print(ptable)
            else:
                console.print(f'[bold red]❌ {param} not found[/] in user-defined table [yellow] {table}[/yellow]')
        else:
            console.print(f'[bold red]❌ {param} not found[/] in user-defined table [yellow] {table}[/yellow]')

    
if __name__ == '__main__':
    app()