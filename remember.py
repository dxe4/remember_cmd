import subprocess
import sys
import os
import pickle

global file_name
file_name = os.path.join(os.path.expanduser("~"), "foo")


class Store:
    def __init__(self):
        self.commands = {}


def load_store():
    if not os.path.exists(file_name):
        store = Store()
        pickle.dump(store, open(file_name, "wb"))
        return store
    else:
        return pickle.load(open(file_name, "rb"))


def save_store(store):
    pickle.dump(store, open(file_name, "wb"))

def exec_command(command: str):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    while proc.poll() is None:
        output = proc.stdout.readline()
        sys.stdout.buffer.write(output)




store = load_store()
#store.commands["hisgrep"] = "history | grep "
#save_store(store)


exec_command("python foo.py")

