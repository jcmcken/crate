import rpm
import os

def get_header(filename):
    ts = rpm.TransactionSet()
    fd = os.open(filename, os.O_RDONLY)
    header = ts.hdrFromFdno(fd)
    os.close(fd)
    return header
