
from malt.newparse.preprocessor import preprocess
from malt.newparse.tokenizer import get_tokens
from malt.newparse.compiler import comp
from malt.malt import serve


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

    print("PREPROCESSOR")
    print(pre)

    token_list = get_tokens(pre)
    print("TOKENIZER")
    for t in token_list:
        if t is None:
            print("===END===")
        else:
            print(t)

    responses = comp(token_list)
    print("COMPILER")
    serve(responses)
