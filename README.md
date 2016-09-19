
# malt
#### a tiny toolkit for structured input and output

## Purpose
Malt provides a set of tools that help with common problems when building
interactive text loops.

## Usage
See `usage.py`. More examples to come later.

## Functions
malt.offer()
malt.serve()
malt.load()

TODO

## Types
Simple options take the form `command arg1, arg2`. By default, all arguments are returned
as literal strings. If you need a specific type of argument, prefix the argument's name
with a type specifier: `command i:arg1, f:arg2`. Malt will try to cast the arguments to
their given types, and will count the input as invalid if they can not be cast.

There are currently five type prefixes:
`s:arg`: string, implied by default
`i:arg`: integer, cast using python's int() function, floors the number if there are decimals
`f:arg`: floats, cast in the same way using float()
`l:arg`: lists, arguments using this form will return a list of space-separated items
`d:arg`: dicts, these args will return a dict using k:v pairs

## Installation
