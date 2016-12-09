
# Malt
#### a toolset for command-driven terminal user interfaces

## Motivation
Programs with command-driven interfaces require a lot of boilerplate to handle
input validation, error checking, and type casting. Malt abstracts this
boilerplate into a small set of easy-to-use functions.

## Usage
```python
import malt
options = [
    'spam',
    'eggs i:count s:style=scrambled',
    'sausages b:spicy=False',
]
while True:
    response = malt.offer(options)
    if response.head == 'spam':
        print('spam, spam, spam, spam')
    elif response.head == 'eggs':
        print((response.style+' eggs ') * response.count)
    elif response.head == 'sausages':
        if response.spicy:
            print("!!!SAUSAGE!!!")
        else:
            print('sausage')
    else:
        pass
```

```
> spam
spam, spam, spam, spam
> eggs 2
scrambled eggs scrambled eggs
> eggs 2 style="over easy"
over easy eggs over easy eggs
> sausage
sausage
> sausage spicy=True
!!!SAUSAGE!!!
> potatoes
[malt] unknown command
```

## Installation
#### Github
```
$ git clone https://github.com/anavros/malt.git malt
$ cd malt
$ pip3 install .
```
#### PyPi
`TODO: upload to pypi`
