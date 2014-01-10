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


def delete_from_store(command=None, key=None, meta_data=None):
    pass


def find_in_store(command=None, key=None, meta_data=None):
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
