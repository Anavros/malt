
from malt.newparse.preprocessor import preprocess
from malt.newparse.tokenizer import get_tokens


def _load_file(path):
    f = open(path, 'r')
    string = f.read()
    f.close()
    return string


def parse(path):
    pass


if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1 and argv[1] == 'parse':
        do_parsing = True
    else:
        do_parsing = False

    raw = _load_file("example.malt")
    pre = preprocess(raw)

    if do_parsing:
        token_list = get_tokens(pre)

    print("PREPROCESSOR")
    print(pre)

    if do_parsing:
        print("TOKENIZER")
        for t in token_list:
            if t is None:
                print("===END===")
            else:
                print(t)
