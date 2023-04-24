import os
import sys
import json
import rich
import typer
import socket
import base64
import subprocess
from typing import Any, List, Dict
from math import floor
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime
from itertools import cycle

from tinydb import TinyDB, Query, where


__all__ = [
    'renderQuery', 'TinyDB', 'Query', 'config', 'cfg',
    'db', 'globals', 'where', 'upsert_param', 'getValue',
    'getKey'
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
"""The tiny database"""

globals = db.table('globals')
"""The global config variable table"""

## Render results in terminal using Rich Tables

def renderQuery(
    results:List[Dict[str,Any]],
    large_columns:List[str]=None,
    first:str = 'param',
    last: str = 'value',
    decode: bool = True,
    ):
    """Renders a TinyDB Query into a Rich Table

    Args:
        results (List[Dict[str,Any]]): Results of a TinyDB Query, in the form of a list of dicts.
        large_columns (List[str], optional): List of columns which should be given more width, 20% of terminal to be exact. Defaults to None.
        first (str, optional): The first column to display in the table. Defaults to 'param'.
        last (str, optional): The last column to display in the table. Defaults to 'value'.

    Raises:
        ValueError: If the results do not correspond to tinydb-like query output, raises ValueError

    Returns:
        rich.Table: A rich renderable with the 
    """
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

    tf = (lambda col : deobfuscate_json(str(col))) if decode else (lambda col : str(col))
    for row in results:
        srow = [tf(row[c]) for c in columns]
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
    """This function obfuscates a JSON object by encoding it as base64 and prepending the string 'OBFS::'
    The JSON object is passed as an argument to the function
    The function converts the JSON object to a string using the json.dumps() method
    The string is then prepended with the string 'OBFS::'
    The function then encodes the string using base64 encoding
    The function then returns the encoded string"""
    strjson = json.dumps(json_data)
    strjson = 'OBFS::'+strjson
    obfuscated = base64.b64encode(strjson.encode('utf-8'))
    return obfuscated.decode('utf-8')


def deobfuscate_json(obfuscated):
    """Deobfuscates a JSON string that has been obfuscated using the obfuscate_json() function.
    
    Parameters
    ----------
    obfuscated : str
        A string that has been obfuscated using the obfuscate_json() function.
    
    Returns
    -------
    dict or list or str
        The deobfuscated JSON string.
    """
    if len(obfuscated) < 4 or len(obfuscated) % 4 == 1:
        return obfuscated
    try:
        decoded = base64.b64decode(obfuscated.encode('utf-8'))
        return json.loads(decoded.decode('utf-8')[6:])
    except Exception as err:
        # wasn't obfuscated using this method, return original value
        return str(obfuscated)

def upsert_param(param:str, value:Any, obfuscate: bool = False):
    '''
    This function is used to upsert a parameter (param) and its corresponding value (value) to the global database.
    The function takes in 3 parameters: param, value, and obfuscate. 
    The param parameter is a string that contains the parameter name. 
    The value parameter can take in any type of value, and it contains the value to be upserted to the database.
    The obfuscate parameter is a boolean value that determines if the parameter and its corresponding value will be obfuscated before being stored in the database.
    The function first creates a Query object called Param.
    It then checks if the obfuscate parameter is set to True. If it is, then the param and value parameters are obfuscated before being stored in the database. 
    If it is not, then the param and value parameters are not obfuscated before being stored in the database.
    The function then upserts the param and value to the database, and also stores the timestamp, machine, and obfuscated parameters.
    '''
    Param = Query()
    if obfuscate:
        obfs_value = obfuscate_json(value)
        obfs_param = obfuscate_json(param)
    else:
        obfs_value = value
        obfs_param = param
    globals.upsert({
        "param": obfs_param,
        "value": obfs_value,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "machine": socket.gethostname(),
        "obfuscated": obfuscate
        },
        Param.param == obfs_param
    )

def getKey(param:str):
    """search for obfuscated params with matching deobfuscated values
    or search for non-obfuscated params with matching values
    return the results"""

    Q = Query()
    returns = globals.search(
        ((Q.param.map(deobfuscate_json) == param) & (Q.obfuscated == True)) |
        ((Q.param == param) & (Q.obfuscated == False))
        )
    return returns

def getValue(param:str, decode:bool = True):
    values = [str(deobfuscate_json(str(p['value']))) if decode else str(p['value']) for p in getKey(param=param)]
    if len(values) > 0:
        if len(values) > 1:
            return values
        else:
            return values.pop()
    else:
        return ''

@cfg.command(name='set', help='Set a config value.', no_args_is_help=True)
@config.command(name='set', help='Set a config value.', no_args_is_help=True)
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
        returns = getKey(param)
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
def lister(
        decode: bool = typer.Option(False,'-k', '--decode', help='Whether to list the obfuscated key/value pairs in clear text')
    ):
    """List all config values. These values are saved in the config tiny database.
    """
    rows = globals.all()
    table = renderQuery(results=rows, decode = decode)

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