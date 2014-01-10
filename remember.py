import subprocess
import sys
import os


def load_file():
    file_name = os.path.join(os.path.expanduser("~"), "foo")
    mode = "a" if os.path.exists(file_name) else "w"
    return open(file_name, mode)


def exec_command(command: str):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    while proc.poll() is None:
        output = proc.stdout.readline()
        sys.stdout.buffer.write(output)


def _write(command, _file):
    _file.write("%s%s" % (command, "\n"))
    _file.flush()


file = load_file()
_write("foo", file)
exec_command("python foo.py")

file.close()
