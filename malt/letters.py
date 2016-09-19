
letters = {}
letters['a'] = r"""
 ||| 
||_||
|| ||
"""
letters['b'] = r"""
|||||
|  _|
|___|
"""
letters['c'] = r"""
|||||
|    
|||||
"""
letters['d'] = r"""
|||||
|   |
|||||
"""
letters['e'] = r"""
|^^^^
|^^^ 
|||||
"""
letters['f'] = r"""
|||||
|||| 
||   
"""
letters['g'] = r"""
|||||
|||||
|||||
"""
letters['h'] = r"""
|   |
|||||
|   |
"""
letters['i'] = r"""
|||||
|||||
|||||
"""
letters['j'] = r"""
|||||
|||||
|||||
"""
letters['k'] = r"""
|||||
|||||
|||||
"""
letters['l'] = r"""
|||||
|||||
|||||
"""
letters['m'] = r"""
|| ||
|^|^|
|   |
"""
letters['n'] = r"""
||  |
|||||
|  ||
"""
letters['o'] = r"""
|||||
|   |
|___|
"""
letters['p'] = r"""
|||||
|||||
|||||
"""
letters['q'] = r"""
|||||
|||||
|||||
"""
letters['r'] = r"""
|||||
|||||
|||||
"""
letters['s'] = r"""
|||||
|||||
|||||
"""
letters['t'] = r"""
|||||
|||||
|||||
"""
letters['u'] = r"""
|||||
|||||
|||||
"""
letters['v'] = r"""
|||||
|||||
|||||
"""
letters['w'] = r"""
|||||
|||||
|||||
"""
letters['x'] = r"""
|||||
|||||
|||||
"""
letters['y'] = r"""
|||||
|||||
|||||
"""
letters['z'] = r"""
|||||
|||||
|||||
"""
letters['0'] = r"""
|||||
|||||
|||||
"""
letters['1'] = r"""
 ||| 
  || 
  || 
"""
letters['2'] = r"""
|||||
|||||
|||||
"""
letters['3'] = r"""
|||||
|||||
|||||
"""
letters['4'] = r"""
|||||
|||||
|||||
"""
letters['5'] = r"""
|||||
|||||
|||||
"""
letters['6'] = r"""
|||||
|||||
|||||
"""
letters['7'] = r"""
|||||
|||||
|||||
"""
letters['8'] = r"""
|||||
|||||
|||||
"""
letters['9'] = r"""
|||||
|||||
|||||
"""
letters['-'] = r"""
     
|||||
     
"""
letters[' '] = r"""
     
     
     
"""

def convert(string):
    base = ["", "", ""]
    for char in string.lower():
        block = letters[char]
        block = block.replace('|', '█')
        block = block.replace('_', '▄')
        block = block.replace('^', '▀')
        block_lines = block.split('\n')[1:-1]
        for i in range(3):
            base[i] += block_lines[i]
            base[i] += ' '
    return '\n'.join(base)
