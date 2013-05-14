import rpm
import os

def get_header(filename):
    ts = rpm.TransactionSet()
    fd = os.open(filename, os.O_RDONLY)
    header = ts.hdrFromFdno(fd)
    os.close(fd)
    return header

def compare_versions(header1, header2):
    return rpm.labelCompare(
        (header1['epoch'], header1['version'], header1['release']),
        (header2['epoch'], header2['version'], header2['release']),
    )
