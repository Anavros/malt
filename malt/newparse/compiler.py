
"""
Compiler stage: probably not the best name.
Takes a stream of tokens and builds a data structure.
"""

from malt.malt import Response
from malt.output import serve

def comp(tokens):
    state = CompilerState()
    for token in tokens:
        # Another thing to note: each token is a separate argument.
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
