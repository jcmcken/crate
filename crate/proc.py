import subprocess
import shlex

def run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen(shlex.split(command), stderr=stderr, stdout=stdout)
    stdout, stderr = proc.communicate()
    code = proc.returncode
    return code, stdout, stderr

