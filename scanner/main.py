import argparse
from pathlib import Path

from intent import scan


def main(**kwargs):
    if 'test' in kwargs['commands']:
        pathlist = Path("tests/cards").glob('**/*.png')
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            scan(path_in_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A service to scan a picture and retrieve contact '
                    'information')
    parser.add_argument('commands', nargs="+", type=str,
                        help="Can be one or many of:"
                             " run (starts the server) / "
                             " test (tests all images in tests/cards')")
    args = parser.parse_args()
    main(**args.__dict__)
