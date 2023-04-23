import os
import sys
import json
import rich
import typer
import socket
import base64
import subprocess
from math import floor
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime
from itertools import cycle

from tinydb import TinyDB, Query, where


__all__ = [
    'renderQuery', 'TinyDB', 'Query', 'config', 'cfg', 'db', 'globals', 'where'
]

console = rich.console.Console()

# directories

current = Path(__file__).parent
static = current / 'static'
absolute_config = Path.home() / '.config' / 'app-name'

static.mkdir(exist_ok=True)
configFile = static / 'config.json'
configFile.touch()

# absolute_config.mkdir(exist_ok=True) # enable this if no absolute path is needed
# configFile = absolute_config / 'config.json'

db = TinyDB(configFile)

globals = db.table('globals')

## Render results in terminal using Rich Tables

def renderQuery(results, large_columns:list=None, first:str = 'param', last: str = 'value'):
    if not large_columns:
        large_columns = ['param', 'value']
    if isinstance(results, (tuple,list)):
        if not len(results):
            return None
        header = results[0]
    elif isinstance(results, dict):
        header = results
        results = [results]
    else:
        raise ValueError(f"Argument must be a list/tuple of dicts, not {type(results)}")
    
    table = Table(show_header=True, header_style="bold blue")

    colors = cycle(['purple4', 'dark_magenta', 'magenta', 'cyan', 'royal_blue1', 'steel_blue1'])

    num_cols = len(header.keys())
    last_column_index = num_cols - 1
    num_large_cols = len(large_columns)
    num_standard_cols = num_cols - num_large_cols

    # Ordering of the keys matters only for key and value
    ordering = lambda value: 0 if value == first else 99999 if value == last else 1
    columns = list(header.keys())
    columns = sorted(columns, key=ordering)

    tsize = os.get_terminal_size()
    width, height = tsize.columns, tsize.lines
    large_width = int(width * 0.2)
    remaining_width = width - large_width * len(large_columns)
    standard_width = floor(remaining_width / num_standard_cols)
    

    for idx, col in enumerate(columns):
        justify = 'left' if idx == 0 else 'right' if idx == last_column_index else 'center'
        if col in large_columns:
            table.add_column(col.capitalize(), width=large_width, justify=justify, style=f"bold {next(colors)}")
        else:
            table.add_column(col.capitalize(), width=standard_width, justify=justify, style=f"{next(colors)}")

    for row in results:
        srow = [row[c] for c in columns]
        table.add_row(*srow)

    return table


config = typer.Typer(
    name='cfg',
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

# utils:

def obfuscate_json(json_data):
    strjson = json.dumps(json_data)
    obfuscated = base64.b64encode(strjson.encode('utf-8'))
    return obfuscated.decode('utf-8')

def deobfuscate_json(obfuscated):
    decoded = base64.b64decode(obfuscated.encode('utf-8'))
    return json.loads(decoded.decode('utf-8'))

@cfg.command(name='set', help='Set a config value.', no_args_is_help=True)
@config.command(name='set', help='Set a config value.', no_args_is_help=True)
def setter(
    param: str = typer.Argument(..., help = 'The parameter to set.'),
    value: str = typer.Argument(..., help='The value to set the parameter to.'),
    ):
    """Set a config value. These values are saved in the config tiny database.
    """
    Param = Query()
    globals.upsert({
        "param": param,
        "value": value,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "machine": socket.gethostname(),
        },
        Param.param == param
    )
    
    console.print(f'[bold green]✅ Set {param} to {value}[/]')

@cfg.command(name='get', help='Get a config value.')
@config.command(name='get', help='Get a config value.')
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
        returns = globals.search(where('param') == param)
        if len(returns):
            table = renderQuery(results=returns)
            if table:
                console.print(table)
            else:
                console.print(f'[bold red]❌ {param} not found[/]')
        else:
            console.print(f'[bold red]❌ {param} not found[/]')

@cfg.command(name='list', help='List all config values.')
@config.command(name='list', help='List all config values.')
def lister():
    """List all config values. These values are saved in the config tiny database.
    """
    rows = globals.all()
    table = renderQuery(results=rows)

    if not table:
        console.print(f'[dim blue]🕵️‍♀️ Seems your settings file is empty[/]')
    else:
        console.print(table)
    
@cfg.command(name='reset', help='Reset all config values.')
@config.command(name='reset', help='Reset all config values.')
def reset():
    """Reset all config values. These values are saved in the config tiny database.
    """
    globals.truncate()
    
    
if __name__ == '__main__':
    config()