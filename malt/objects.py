
class Response:
    """
    A `Response` object stores information about user input, taken as a response
    to a prompt. The object stores the input, after it has been verified and
    validated, as well as metadata about the input's context. The first word of
    the user's response, the command, or head, can be compared directly to the
    response object using '=='. A new response is generated for each input.
    """
    def __init__(self,
        head=None,
        body=None,
        raw_args=None,
        raw_kwargs=None,
        valid=False,
        empty=False,
        error=None,
        noncommand=False,
        options=None
    ):

        self.head = head if valid else None
        self.body = body
        if body is not None:
            for k, v in body.items():
                self.__dict__[k] = v

        # new params
        self.valid = valid
        self.noncommand = noncommand
        self.empty = empty
        self.error = error
        self.options = options

        self.raw_head = head
        self.raw_args = raw_args if raw_args else []
        self.raw_kwargs = raw_kwargs if raw_kwargs else {}

    def __eq__(self, x):
        """
        Directly comparing a response to a string is being deprecated.
        Compare response.head instead.
        """
        return self.head == x

    def __str__(self):
        return self.raw_head

    def __repr__(self):
        return self.__str__()
