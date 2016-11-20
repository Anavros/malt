
class Response:
    """
    Easily-accessible user input stored with metadata.
    """
    def __init__(self, head, body):
        self.head = head
        self.body = body

        # Put arguments in body for easy access.
        for k, v in self.body.items():
            self.__dict__[k] = v

    def __iter__(self):
        for k, v in self.body.items():
            yield k, v

    def __repr__(self): return self.head
    def __str__(self): return self.__repr__()
    def __len__(self): return len(self.body)


class UserInput:
    """
    Iterable storage of user input tokens used for parsing.
    """
    def __init__(self, head, body):
        self.head = head  # first word in the string
        self.body = body  # list of (key, value) args, ordered

    def __iter__(self):
        for item in self.body:
            yield item

    def __len__(self): return len(self.body)

    def get(self, index, key):
        """
        """
        pass

    def lookup(self, key):
        """
        Return first value associated with key. There may be duplicates!
        """
        for k, v in self.body:
            if k == key:
                return k, v
        raise KeyError("Item not found.")


class Signature:
    """
    An orderly representation of an option string used for parsing.
    """
    def __init__(self, head, body):
        self.head = head  # first word in the string
        self.body = body  # list of (key, value) args, ordered

    def __iter__(self):
        for item in self.body:
            yield item

    def __len__(self):
        return len(self.body)

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
    def __init__(self, position, key, value, cast):
        self.position = position
        self.key = key
        self.value = value
        self.cast = cast
