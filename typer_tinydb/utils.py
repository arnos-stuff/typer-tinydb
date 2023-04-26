import os
import sys
import json
import socket
import rich
import base64
from math import floor
from pathlib import Path
from datetime import datetime
from tinydb import TinyDB, where, Query
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from itertools import cycle


__all__ = [
    "console", "current", "static", 'absolute_config',
    'configFile', 'db', 'globals', 'renderQuery', 'obfuscate_json',
    'deobfuscate_json', 'upsert_param', 'getKey', 'getValue',
    'getUserTable', 'create_table', 'drop_table', 'ugetKey', 'ugetValue',
    'upsert_param_udb', 'renderAllTables'
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

_tables = db.table('USER-DEFINED-TABLES')
"""User-defined databases"""

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


def obfuscate_json(json_data):
    """This function obfuscates a JSON object by encoding it as base64 and prepending the string 'OBFS::'
    The JSON object is passed as an argument to the function
    The function converts the JSON object to a string using the json.dumps() method
    The string is then prepended with the string 'OBFS::'
    The function then encodes the string using base64 encoding
    The function then returns the encoded string
    
    Args:
        json_data (dict): any nested dict or literal to be obfuscated
        
    Returns:
        (str) obfuscated base64 string encoding
        """
    strjson = json.dumps(json_data)
    strjson = 'OBFS::'+strjson
    obfuscated = base64.b64encode(strjson.encode('utf-8'))
    return obfuscated.decode('utf-8')


def deobfuscate_json(obfuscated):
    """Deobfuscates a JSON string that has been obfuscated using the obfuscate_json() function.
    
    Args:
        obfuscated : str
            A string that has been obfuscated using the obfuscate_json() function.
    
    Returns:
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
    
def tabCallback(table: TinyDB = ..., msg: str = ...):
    tres = table.all()
    tabr = renderQuery(tres)
    
    if len(tres):
        console.print(Rule(msg))
        console.print(tabr)
        console.print('\n')
    else:
        console.print(Panel("🕵️‍♂️ looks like your table is empty ...", style='dim blue'))
        
def renderAllTables():
    gres = globals.all()
    console.print(Rule("All variable listing enabled"))
    console.print(Rule('[bold red] Global variables table [/bold red]'))
    console.print(renderQuery(gres))
    console.print('\n\n')
    
    all_tables = _tables.all()
    
    colors = cycle(['purple4', 'dark_magenta', 'hot_pink', 'cyan', 'royal_blue1', 'steel_blue1'])
    
    for tb in filter(lambda tbdata: tbdata['active'], all_tables):
        cl = next(colors)
        tabCallback(db.table(tb['name']), f"[bold {cl}] User-defined database '{tb['name']}' [/bold {cl}]")
        console.print('\n\n')

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
    
def create_table(table: str = ..., schema: dict = None):
    """
    Create a table with the given name and schema. If the table already exists, the schema is updated.
    """
    
    if len(_tables.search(where('name') == table.lower().strip())):
       console.log(f'[red1] {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} [/red1] | [dark_orange3] User-defined table "{table}"[/dark_orange3] [bold red] already exists [/bold red]') 
    else:
        utable = db.table(table.lower().strip())
        console.log(f'[green] {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} [/green] | [yellow] Created user-defined table "{table}"[/yellow]')

    _tables.upsert({
        'name' : table.lower().strip(),
        'created_on' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "machine": socket.gethostname(),
        'active': True,
        'strict':False,
        'schema': schema or {}
    },
    where('name') == table.lower().strip()
    )

def drop_table(table: str = ..., rm: bool = False):
    """This code is used to drop a table from the database. It is used when the user wants to drop a table from the database. The user can choose to either remove the table entirely or just deactivate it. If the user chooses to deactivate the table, then the table will still exist in the database but will be inactive, meaning it can't be accessed by users. If the user chooses to remove the table, the table will be completely removed from the database.
    """
    assert isinstance(table, str), 'table must be a string'
    assert isinstance(rm, bool), 'rm must be a boolean'
    if not rm:
        # deactivate the table
        _tables.upsert({
        'active': False,
        },
        where('name') == table.lower().strip()
        )
    else:
        # remove table
        db.drop(table.lower().strip())
        # remove table from _tables table
        _tables.delete(where('name') == table.lower().strip())
    
def getUserTable(table: str = ...):
    """Returns the user table object for the given table name.
    
    Arguments:
        table -- the name of the table to return
    
    Returns:
        (TinyDB | None): when the user-defined DB can be found it returns a TinyDB object, else None is returned
    """
    table = table.lower().strip()
    udb = _tables.search( (where('name') == table) & (where('active') == True) )
    
    if len(udb):
        metadata = udb.pop()
        if metadata and metadata['active']:
            return db.table(metadata['name'])
        else:
            return None
    else:
        return None

def ugetKey(param:str, table:str):
    """
    Function `ugetKey`. It takes two parameters, the `param` and the `table`. The `param` is the parameter that we want to search for in the table, and the `table` is the table that we want to search in.

    The first thing that we do is check if the table is valid. If it is, we search for the param in the table. If the param is obfuscated, we deobfuscate it before searching. If we find the param, we return the key. If we don't find it, we return a 404 error.
    
    Args:
        param (str): The parameter, or key, to be retrieved
        table (str): The user-defined table from which it is retrieved.
        
    
    """
    # Check if the table is valid
    udb = getUserTable(table)
    if udb is not None:
        # If the param is obfuscated, we deobfuscate it before searching
        Q = Query()
        returns = udb.search(
            ((Q.param.map(deobfuscate_json) == param) & (Q.obfuscated == True)) |
            ((Q.param == param) & (Q.obfuscated == False))
            )
        if returns:
            return returns
        else:
            return 403
    else:
        return 404
    
def ugetValue(param:str, table:str, decode:bool = True):
    # Get the value from the key
    values = [str(deobfuscate_json(str(p['value']))) if decode else str(p['value']) for p in ugetKey(param=param) if p != 404]
    # If there are no values, return None
    if len(values) > 0:
        # If there are more than one value, return the values
        if len(values) > 1:
            return values
        else:
            # If there is only one value, return that value
            return values.pop()
    else:
        return None
    
def upsert_param_udb(table: TinyDB, param: str = ..., value:Any = ..., obfuscate: bool = False):
    
    Param = Query()
    if obfuscate:
        obfs_value = obfuscate_json(value)
        obfs_param = obfuscate_json(param)
    else:
        obfs_value = value
        obfs_param = param
    table.upsert({
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
    """The getValue function is used to get the deobfuscated value of the parameter. If there are multiple deobfuscated values, the first one is returned. If there is only one deobfuscated value, it is returned. If there are no deobfuscated values, an empty string is returned. The getKey function is used to get the parameter values, and then the deobfuscate_json function is used to deobfuscate the values.

    Args:
        param (str): The name of the parameter to get the value of.
        decode (bool, optional): Whether or not to deobfuscate the value. Defaults to True.

    Returns:
        str: The deobfuscated value of the parameter.
    """
    # Get the parameter values
    values = [str(deobfuscate_json(str(p['value']))) if decode else str(p['value']) for p in getKey(param=param)]
    if len(values) > 0:
        if len(values) > 1:
            # If there are multiple values, return the first one
            return values
        else:
            # If there is only one value, return it
            return values.pop()
    else:
        # If there are no values, return an empty string
        return ''