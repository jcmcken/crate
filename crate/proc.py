import subprocess
import shlex

def run(command, cwd=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen(shlex.split(command), stderr=stderr, stdout=stdout,
        cwd=cwd)
    stdout, stderr = proc.communicate()
    code = proc.returncode
    return code, stdout, stderr

