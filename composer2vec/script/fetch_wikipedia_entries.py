import argparse
import os

import progressbar

from data import csv, wikipedia


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help='Path to composers CSV file')
    parser.add_argument('directory', help='Directory to store data')

    return parser.parse_args()


def main():
    args = _parse_args()

    for composer in progressbar.progressbar(csv.composers(args.path)):
        composer_id = composer[0]
        url = composer[-1]
        text = wikipedia.text(wikipedia.soup(url))

        path = os.path.join(args.directory, '{}.txt'.format(composer_id))
        with open(path, 'w') as f:
            f.write(text)
