
from malt.objects import Response
from malt.constants import DEFAULT_ARG_SETTER

"""
Compiler stage: probably not the best name.
Takes a stream of tokens and builds a data structure.
"""


# NOTE: this step will need to get more complicated
# when we start to allow implied kwargs without '=' markers
def build(tokens):
    response = Response()
    previous_kwarg_key = None
    for token in tokens:
        if not response.raw_head:
            # The first keyword is the head of the line.
            response.raw_head = token
        elif previous_kwarg_key:
            # If the previous argument was a k:v pair, use this as the value.
            response.raw_kwargs[previous_kwarg_key] = token
            previous_kwarg_key = None
        elif DEFAULT_ARG_SETTER in token:
            # If '=' found, this and the next arg are a k:v pair.
            token = token.rstrip(DEFAULT_ARG_SETTER)
            response.raw_kwargs[token] = None
            previous_kwarg_key = token
        else:
            # Otherwise it's just a normal positional argument.
            response.raw_args.append(token)
    return response


# Only take one line at a time!
def comp(tokens):
    state = CompilerState()
    for token in tokens:
        # Another thing to note: each token is a separate argument.
        if DEFAULT_ARG_SETTER in token:
            pass
        if token == '=':
            state.pending_keyword = state.response.raw_args.pop()

        elif token is None:  # Nones signify new lines.
            state.cut()

        else:
            if state.pending_keyword:
                state.response.raw_kwargs[state.pending_keyword] = token
                state.pending_keyword = ''
            else:
                if state.new_line:
                    state.response.raw_head = token
                    state.new_line = False
                else:
                    state.response.raw_args.append(token)
    return state.lines


class CompilerState:
    def __init__(self):
        self.lines = []
        self.new_line = True
        self.response = Response(valid=False)
        self.pending_keyword = ''

    def cut(self):
        self.lines.append(self.response)
        self.response = Response(valid=False)
        self.new_line = True
