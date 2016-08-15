#!/usr/bin/env python3

import single as malt

def main():
    little_options = ['add', 'subtract', 'echo', 'load']
    options = [
        "add int(n) int(m)",
        "dashes",
        "echo string",
        "load",
        "div anchor[top|bottom]"
    ]
    big_options = [
        """
        ADD     # Add two numbers together.
        int(n)  # The first number.
        int(m)  # The second number.
        """,
        """
        SUBTRACT int(n) int(m)
        # Subtract the second number from the first.
        """,
        """
        ECHO
        string  # A string to be echoed.
        """,
        """
        LOAD    # Load the example language.
        """,
        """
        DIV
        anchor=[top|bottom|left|right]
        """,
        """
        SIZE
        float(percent[0-1])
        """
        "TEST # A comment test."
    ]
    while True:
        response = malt.offer(options) 
        if response == "add":
            malt.serve(response.n + response.m)

        elif response == "subtract":
            malt.serve("---")

        elif response == "echo":
            malt.serve(response.string)

        elif response == "load":
            malt.serve(malt.harvest('example.lang'))

if __name__ == "__main__":
    main()
