from crate.managers.file import FileManager
from crate.managers.rpm import RpmManager

MANAGERS = {
  'file': FileManager,
  'rpm': RpmManager,
}

def duplicate_destinations(managers):
    return False
    dest_map = {}
    for m in managers:
        pass
    return len(list(set(destinations))) == len(destinations)
