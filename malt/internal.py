
tabs = 0
tab_width = 4
blessed = False


def mprint(*args, end='\n'):
    if blessed:
        print('(bless) ', *args, end=end)
    else:
        print('(curse) ', *args, end=end)


def minput(prompt):
    if blessed:
        return input('(bless) '+prompt)
    else:
        return input('(curse) '+prompt)
