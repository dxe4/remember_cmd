import subprocess
import sys
import os
import pickle

global file_name
file_name = os.path.join(os.path.expanduser("~"), "foo")


class Store:
    def __init__(self):
        self.commands_dict = {}
        self.commands_list = []


def load_store():
    if not os.path.exists(file_name):
        store = Store()
        pickle.dump(store, open(file_name, "wb"))
        return store
    else:
        return pickle.load(open(file_name, "rb"))


def save_store(store: Store):
    pickle.dump(store, open(file_name, "wb"))


def appent_to_store(command, key=None, meta_data=None):
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
    @param key: When key is used it will be saved in a key value store
    @param meta_data: When metadata is used you will be able to search by metadata too
    """
    pass


def delete_from_store(command=None, key=None, meta_data=None, regex=False):
    """
        Delete command(s) from store.
        Multiple values can be deleted if regex mode is used,
            or if the exactly the same meta_data exists in more than one commands
    @param command: If command is given the command(s) will be deleted.
    @param key: If key is given the command corresponding to that key will be deleted
    @param meta_data: If meta_data is given the command(s) corresponding to meta_data will be deleted
    @param regex: If regex is set to true the command and meta_data will be used as regex
            and multiple commands may be deleted at once
    """
    pass


def find_in_store(command=None, key=None, meta_data=None, regex=False):
    """
        Find commands from store.
        Multiple values can be found if regex mode is used,
            or if the exactly the same meta_data exists in more than one commands
    @param command: If command is given will try to find the corresponding command(s)
    @param key: If key is given the command matching the key will be returned
    @param meta_data: If metadata is given the corresponding command(s) will be returned
    @param regex: If regex mode is given meta_data and command will be used as regex
    @return The found command(s)
    """
    pass


def exec_command(command: str):
    # TODO later use for --exec parameter
    # exec_command("python foo.py")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    while proc.poll() is None:
        output = proc.stdout.readline()
        sys.stdout.buffer.write(output)

local_store = load_store()
#store.commands["hisgrep"] = "history | grep "
#save_store(store)
