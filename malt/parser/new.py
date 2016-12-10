
from malt.constants import *
from malt.exceptions import MaltSyntaxError
from malt.objects import Argument, Signature

import logging
logging.basicConfig(filename="parser.log", level=logging.DEBUG)
logging.info("Starting parser log.")


# Steps:
# "stream 3 [words and things] key=value xs=[]"
# ["stream", "3", "[words and things]", "key=value", "xs=[]"]
# [(None, "stream"), (None, "3"), (None, "[words and things]"),
# ("key", "value"), ("xs", "[]")]
# ["stream", 3, ["words", "and", "things"], ("key", "value"), ("xs", [])]

# Stack-Based Parsing
# hello [is 'it really' me] 'youre looking for?'


def parse(text):
    return Signature()


class Token:
    def __init__(self, string):
        if EQUALS in string:
            self.key, self.val = string.split(EQUALS, 1)
        else:
            self.key, self.val = None, string


class Stack:
    def __init__(self):
        self.chars = []

    def enclosed(self):
        """
        The stack is considered enclosed if there is at least one unresolved
        opening bracket or quote.
        """
        return len(self.chars) > 0

    def push(self, char):
        """
        Add a char to the stack. If it matches the previously pushed char,
        cancel the two out, removing the enclosure.
        """
        if self._match(char):
            self.chars.pop()
        else:
            self.chars.append(char)

    def _match(self, c):
        """
        Does the last character in the stack syntactically match the new one?
        For example: [ + ], ' + ', { + }
        """
        if not self.chars:
            return False
        prev = self.chars[-1]
        if prev == LIST_BEGIN:
            return c == LIST_END
        elif prev == DICT_BEGIN:
            return c == DICT_END
        elif prev in QUOTES:
            return c == prev


def tokenize(line):
    """
    Separate one line into string tokens.
    """
    tokens = []
    buffer = ""
    braces = Stack()
    for c in line:
        if c in SEPARATORS:
            if not braces.enclosed():
                tokens.append(buffer)
                buffer = ""
                continue  # don't add char to buffer
            # If enclosed, just add the literal character.
        elif c in QUOTES+BRACES:
            braces.push(c)
        buffer += c
        logging.debug("adding '{}' to buffer; buffer = {}; stack = {} ".format(
            c, buffer, braces.chars))
    tokens.append(buffer)
    return tokens


def convert(tokens):
    """
    Turn a list of tokens into a signature.
    """
    try:
        head = tokens.pop(0)
    except IndexError:
        return Signature("", [])

    body = []
    for i, token in enumerate(tokens):
        body.append(Argument(i, token.key, token.val, None))
    #[Argument(i, t.key, t.val, None) for i, t in enumerate(tokens)]
    return Signature(head, body)
