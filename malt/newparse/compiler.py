
"""
Compiler stage: probably not the best name.
Takes a stream of tokens and builds a data structure.
"""

from malt.malt import Response

def comp(tokens):
    state = CompilerState()
    for token in tokens:
        # Another thing to note: each token is a separate argument.
        if token is not None:  # Nones signify new lines.
            state.response.raw_args.append(token)
        else:
            state.cut()
    return state.lines


class CompilerState:
    def __init__(self):
        self.lines = []
        self.response = Response(valid=False)

    def cut(self):
        self.lines.append(self.response)
        self.response = Response(valid=False)
