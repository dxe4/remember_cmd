import subprocess
import sys
import os
import argparse
import sqlite3
from collections import OrderedDict
from itertools import combinations, starmap

# TODO consider service running at startup not sure if it worths doing yet


def append_to_store(command, add_key=None, add_meta_data=None):
    """
        Appends a command in the store.
        You can retrieve the command back in 3 different ways:
            1) Search the actual command
                e.g. command is history | grep foo, you can search all commands for foo
            2) Save a key for the command
                e.g. command is ps -aux you can add a key 1, then you can retrieve it by giving one
            3) Save metadata
                e.g. command is pip install -r requirements.txt
                and metadata is "use pip and requirements.txt to install dependencies"
                Then you can search by "requirements.txt" or by "dependencies"

    @param command: The command to save
    @param add_key: When key is used it will be saved in a key value store
    @param add_meta_data: When metadata is used you will be able to search by metadata too
    """
    pass


def delete_from_store(command=None, remove_key=None, remove_metadata=None, regex=False):
    """
        Delete command(s) from store.
        Multiple values can be deleted if regex mode is used,
            or if the exactly the same meta_data exists in more than one commands
    @param command: If command is given the command(s) will be deleted.
    @param remove_key: If key is given the command corresponding to that key will be deleted
    @param remove_metadata: If meta_data is given the command(s) corresponding to meta_data will be deleted
    @param regex: If regex is set to true the command and meta_data will be used as regex
            and multiple commands may be deleted at once
    """
    pass


def find_in_store(command=None, search_key=None, search_metadata=None, regex=False):
    """
        Find commands from store.
        Multiple values can be found if regex mode is used,
            or if the exactly the same meta_data exists in more than one commands
    @param command: If command is given will try to find the corresponding command(s)
    @param search_key: If key is given the command matching the key will be returned
    @param search_metadata: If metadata is given the corresponding command(s) will be returned
    @param regex: If regex mode is given meta_data and command will be used as regex
    @return The found command(s)
    """
    pass


class DB:
    def __init__(self):
        self.db_name = os.path.join(os.path.expanduser("~"), "remember_cmd.db")
        if not self.exists():
            self.conn = self.create()
        else:
            self.conn = self.connect()

    def exists(self):
        return os.path.exists(self.db_name)

    def connect(self):
        return sqlite3.connect(self.db_name)

    def disconnect(self):
        if not self.conn:
            raise Exception("Connection doesn't exist can't disconnect")
        self.conn.close()

    def insert(self, _dict: dict):
        _dict = OrderedDict(_dict)
        keys, values = _dict.keys(), _dict.values()
        cursor = self.conn.cursor()
        query = "INSERT INTO command ('%s') VALUES %s" \
                % ("','".join(keys), str(tuple("?" * len(values))))
        cursor.execute(query, values)

    def create(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE commands(
                id INTEGER PRIMARY KEY,
                key VARCHAR(150) DEFAULT NULL,
                metadata VARCHAR(350) DEFAULT NULL,
                deleted TINYINT DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.close()
        conn.commit()
        return conn


class ArgHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.arg_type_dict = {}
        # argparse provides groups for arg dependencies but in this case it would
        # be a lot of dirty code
        self.dependant_args = {
            "add_key": ("command", "from_history"),
            "add_metadata": ("command", "from_history"),
            "exec": ("find_history", "search_key",
                     "search_metadata", "search"),
            "exec_safe": ("find_history", "search_key",
                          "search_metadata", "search"),
            "regex": ("search", "remove", "search_metadata",
                      "remove_metadata", "search_key", "remove_key"),
        }

        self.add("command_args", "-c", "--command",
                 help="Specify command",
                 type=str, nargs=1)

        self.add("command_args", "-fh", "--from_history",
                 help="Adds a command from history e.g. remember -fh -1 -ak foo ",
                 type=int, nargs=1)

        self.add("add_args", "-ak", "--add_key",
                 help="Add command using a key e.g. remember -c history -ak his",
                 type=str, nargs=1, metavar="KEY")

        self.add("delete_args", "-rk", "--remove_key",
                 help="Remove command using a key e.g. remember -rk his",
                 type=str, nargs=1, metavar="KEY")

        self.add("search_args", "-sk", "--search_key",
                 help="Search command using a key e.g. remember -sk his",
                 type=str, nargs=1, metavar="KEY")

        self.add("add_args", "-am", "--add_metadata",
                 help="Add metadata to the command e.g. remember -c history -am history of commands",
                 type=str, nargs=1, metavar="METADATA")

        self.add("delete_args", "-rm", "--remove_metadata",
                 help="Remove metadata from command e.g. remember -c history -rm of commands",
                 type=str, nargs=1, metavar="METADATA")

        self.add("search_args", "-sm", "--search_metadata",
                 help="Search for commands with metadata e.g. remember -sm of commands",
                 type=str, nargs=1, metavar="METADATA")

        self.add("add_args", "-a", "--add",
                 help='Add command without information e.g. remember -a "history | grep foo"',
                 type=str, nargs=1, metavar="COMMAND")

        self.add("delete_args", "-r", "--remove",
                 help='Remove command e.g. remember -r "history | grep foo"',
                 type=str, nargs=1, metavar="COMMAND")

        self.add("search_args", "-s", "--search",
                 help='Search command e.g. remember -s history -R (see regex for R)',
                 type=str, nargs=1, metavar="COMMAND")

        self.add("other_args", "-R", "--regex",
                 help="use args as a regex for searching) e.g. remember -sk foo -R",
                 action='store_true', default=False)

        self.add("exec_args", "-e", "--exec",
                 help="Execute the command found. If more than one found will prompt to choose",
                 action='store_true', default=False)

        self.add("exec_args", "-es", "--exec_safe",
                 help="Execute the command found but prompt before executing "
                      "(showing the command to be executed and asking for confirmation)"
                      "If more than one found will prompt to choose",
                 action='store_true', default=False)

        self.add("other_args", "-l", "--list",
                 help="List all commands e.g. remember -l",
                 action='store_true', default=False)

        self.args = vars(self.parser.parse_args())

    def add(self, arg_type, *args, **kwargs):
        arg = self.parser.add_argument(*args, **kwargs)
        self.arg_type_dict[arg.dest] = arg_type

    def state_validation(self):
        dependant_keys = [key for key in self.dependant_args.keys()
                          if self.args[key]]
        # no dependant keys we can go on
        if not dependant_keys:
            return []

        for key in dependant_keys:
            # case dependant keys
            # don't have any of the dependant args
            if not [val for val in self.dependant_args[key]
                    if self.args[val]]:
                return dependant_keys
        return []

    def get_input(self):
        """
            Get all the command line args as given by the user
        @return: dict: Args given by the user in the form name : {value, type}
                example: {'list': (True, 'other_args')}
        """
        return {arg: (value, self.arg_type_dict[arg])
                for arg, value in self.args.items() if value}


def exec_command(command: str):
    # TODO later use for --exec parameter
    # exec_command("python foo.py")
    procedure = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    while procedure.poll() is None:
        output = procedure.stdout.readline()
        sys.stdout.buffer.write(output)


class InputProcessor():
    def __init__(self, _args: dict):
        self._args = _args
        self.command = self._get_command()
        self.search = self._get_other("search_args")
        self.insert = self._get_other("add_args")
        self.delete = self._get_other("delete_args")
        self.other = self._get_other("other_args")
        _and = lambda x, y: x and y
        if any(starmap(_and, combinations([self.search, self.insert, self.delete], 2))):
            raise Exception("Invalid state, run remember -h")
        print(self.command)
        print(self.search)
        print(self._args)

    def _get_command(self):
        try:
            return next((v[0][0] for v in self._args.values() if v[1] == "command_args"))
        except StopIteration:
            return None

    def _get_other(self, to_check: str):
        return {k: v[0][0] for k, v in self._args.items() if v[1] == to_check}

    def process(self):
        _kwargs = {}  # TODO setup
        if self.search:
            find_in_store(self.command)
        if self.delete:
            delete_from_store()
        if self.insert:
            append_to_store(self.command)


if __name__ == "__main__":
    arg_handler = ArgHandler()
    _args = arg_handler.get_input()
    if arg_handler.state_validation():
        raise NotImplementedError("Need to give a proper warning which args have dependencies")
    if not _args:
        arg_handler.parser.print_help()
    input_processor = InputProcessor(_args)
    db = DB()
#store.commands["hisgrep"] = "history | grep "
# save_store(store)
