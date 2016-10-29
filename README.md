
# Malt
#### a toolset for making fantastic interactive loops

## Benefits
When you include malt in your interactive text program, it will type-check your input, format your output, parse your config files, and log information wherever it needs to go.

## Usage
```python
import malt
malt.log("Starting example...")
malt.serve("Hello, there!")
options = [
    'spam',
    'eggs i:count s:style=scrambled',
    'sausages b:spicy',
]
while True:
    response = malt.offer(options)
    if response.head == 'spam':
        malt.serve('spam')
    elif response.head == 'eggs':
        malt.serve((response.style+' eggs') * response.count)
    elif response.head == 'sausages':
        if response.spicy:
            malt.log("This one's a feisty breakfaster, they are!", level='GOSSIP')
        else:
            malt.log("Boring old mild-sausage-haver here.", level='GOSSIP')
        malt.serve('sausage')
    else:
        malt.handle(response)
```

## Functionality
```python
>>> malt.serve('sausages')
sausages
>>> malt.serve(['spam', 'eggs'])
[
    [0] spam
    [1] eggs
]
>>> malt.serve({'breakfast_foods': ['spam', 'eggs', 'ham'], 'daily': 'sausages'}, compact=True)
    breakfast_foods:
        [0] spam
        [1] eggs
        [2] ham
    daily: sausages
```
Malt makes data structures easy to read. Items passed to `malt.serve` are formatted according to their types in order to create consistent, nicely-organized output.
```python
>>> malt.log("I'll have the spicy sausages today.")
[LOG] I'll have the spicy sausages today.
>>> gossip_log = open('.gossip', 'w')
>>> malt.redirect('GOSSIP' gossip_log)
>>> malt.log("Someone's getting spicy.", level='GOSSIP')
(in .gossip):
[GOSSIP] Someone's getting spicy.
>>> malt.log("Sausages, coming up!", show_level=False)
Sausages, coming up!
```
Malt features a simple logging tool. `malt.log` formats output in the same way as `serve`, but additionally allows the user to associate a level with each message. Log levels can be hidden, shown, and redirected.

`TODO` More details.

## Installation
Coming soon.
