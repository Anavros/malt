
import argparse

def main(language_file, syntax_file, options=None):
    if options is None:
        options = []
    with open(language_file, 'r') as f:

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("lang_file")
    main(parser.parse_args())
