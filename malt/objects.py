
class Response:
    """
    Easily-accessible user input stored with metadata.
    """
    def __init__(self, head, body, text):
        self._head = head
        self._body = body
        self._text = text

        for k, v in body.items():
            self.__dict__[k] = v

    def __eq__(self, x):
        return self._head == x

    def __iter__(self):
        for k, v in self._body.items():
            yield k, v

    def __repr__(self):
        return self._head

    def __len__(self):
        return len(self._body)


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
