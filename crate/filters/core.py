import re

class Filter(object):
    allowed_modes = ['allow', 'deny']

    def __init__(self, name, mode='allow', args = []):
        self.name = name
        self.mode = mode
        self.args = args

    def allow(self, item):
        return self.matches(item)

    def deny(self, item):
        return not self.matches(item)

    def filter(self, item):
        transformed = self.transform(item)
        mode_func = getattr(self, self.mode)
        return mode_func(transformed)

    def preprocess_args(self):
        """
        Preprocess ``self.args`` before doing any filtering against them.

        This method should update ``self.args`` in place.
        """
        pass

    def transform(self, item):
        """
        Transform ``item`` before comparing against the filter args.

        Default behavior is identity -- don't transform.

        Should return an object.
        """
        return item

    def matches(self, item):
        """
        Take ``item``, which was transformed using ``self.transform``, and
        check if it exists in the filter args.
        
        Should return a boolean value.
        """
        return NotImplementedError

class BelongsToFilter(Filter):
    def matches(self, item):
        return item in self.args

class RegexFilter(Filter):
    def preprocess_args(self):
        self.args = map(re.compile, self.args)

    def matches(self, item):
        for regex in self.args:
            if regex.search(item):
                return True
        return False
        
