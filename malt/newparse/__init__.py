
from malt.newparse.preprocessor import preprocess
from malt.newparse.tokenizer import get_tokens
from malt.newparse.compiler import comp
from malt.newparse.validator import validate, generate_signatures

# TEMP::
from malt import out


def _load_file(path):
    with open(path, 'r') as f:
        string = f.read()
    return string


def test(raw_file, options, show_steps):
    sigs = generate_signatures(options)
    if 'signatures' in show_steps:
        print("SIGNATURES")
        for k, v in sigs.items():
            print(k, v)
    preprocessed = preprocess(raw_file)
    if "preprocessor" in show_steps:
        print("PREPROCESSOR")
        print(preprocess(raw_file))
    token_list = get_tokens(preprocessed)
    if "tokenizer" in show_steps:
        print("TOKENIZER")
        for t in token_list:
            if t is None:
                print("===END===")
            else:
                print(t)
    responses = comp(token_list)
    if "compiler" in show_steps:
        print("COMPILER")
        for r in responses:
            out(r)
    validated = validate(responses, options)
    if "validator" in show_steps:
        print("VALIDATOR")
        for v in validated:
            out(v)


if __name__ == '__main__':
    raw = _load_file("example.malt")
    options = [
        'empty',
        'one argument',
        'default argument=default',
        'types i:int f:float s:string b:bool',
        'fancy [s]:list_of_strings {s-i}:map_of_strings_to_ints',
    ]
    steps = [
        #'preprocessor',
        #'tokenizer',
        #'compiler',
        #'validator',
        #'signatures',
    ]
    test(raw, options, steps)
