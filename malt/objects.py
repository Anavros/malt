
class Response:
    """
    Easily-accessible user input stored with metadata.
    """
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __iter__(self):
        for item in self.body:
            yield item

    def __repr__(self): return self.head
    def __str__(self): return self.__repr__()
    def __len__(self): return len(self.body)


# sig.get(0)
# sig.get('key')
class Signature:
    """
    An orderly representation of an option string used for parsing.
    """
    def __init__(self, raw):
        self.raw = raw  # the raw option string, used for help messages
        self.head = ""  # first word in the string
        self.body = []  # list of (key, value) args, ordered

    def __repr__(self):
        return "HEAD: {}, ARGS: {}, KWARGS: {}".format(
            self.head, self.args, self.kwargs)

    def __iter__(self):
        for item in self.body:
            yield item

    # TODO: what about casts?
    def add(self, key, value=None):
        """
        Add an argument to the signature. Maintains order of arguments.
        Optionally specify a default value for a parameter, like a kwarg.
        """
        # Using a list of pairs to maintain order.
        self.body.append((key, value))

    def get(self, x):
        """
        Return the value matched to x. Uses position if x is an int, otherwise
        treats x like dict key.
        """
        if type(x) is int:
            return self.body[x]
        else:
            return self.lookup(x)

    def lookup(self, key):
        """
        Return first value associated with key. There may be duplicates!
        """
        for k, v in self.body:
            if k == key:
                return k, v
        raise KeyError("Item not found.")


class Argument:
    def __init__(self, raw, key, cast, default):
        self.raw = raw
        self.key = key
        self.cast = cast
        self.default = default

    def __repr__(self):
        if self.default:
            return "def={} ({})".format(self.default, self.cast)
        else:
            return "{} ({})".format(self.key, self.cast)
