
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

    raw = _load_file("example.malt")
    pre = preprocess(raw)
    token_list = get_tokens(pre)

    print("PREPROCESSOR")
    print(pre)

    print("TOKENIZER")
    for t in token_list:
        if t is None:
            print("===END===")
        else:
            print(t)
