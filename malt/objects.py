
class Response:
    """
    Easily-accessible user input stored with metadata.
    """
    def __init__(self, head, body):
        self.head = head
        self.body = body

        # Put arguments in dict for easy access.
        for k, v in self.body.items():
            self.__dict__[k] = v

    def __iter__(self):
        for k, v in self.body.items():
            yield k, v

    def __repr__(self): return self.head
    def __str__(self): return self.__repr__()
    def __len__(self): return len(self.body)


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


class Argument:
    def __init__(self, position, key, value, cast):
        self.position = position
        self.key = key
        self.value = value
        self.cast = cast
