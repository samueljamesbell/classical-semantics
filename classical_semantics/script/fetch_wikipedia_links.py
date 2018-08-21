import argparse
import collections

import progressbar

from classical_semantics.data import csv, wikipedia


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('source_path', help='Path to composers CSV file')
    parser.add_argument('target_path', help='Path to target CSV file')

    return parser.parse_args()


def main():
    args = _parse_args()

    all_composers = list(csv.composers(args.source_path))
    name_to_composer_id = {c[1]: c[0] for c in all_composers}

    triples = []

    for composer in progressbar.progressbar(all_composers):
        source_id, *_, url = composer

        target_names = wikipedia.link_titles(wikipedia.soup(url))
        target_ids = [name_to_composer_id[name] for name in target_names
                      if name in name_to_composer_id]

        for target_id, count in collections.Counter(target_ids).most_common():
            triples.append((source_id, target_id, count))

    with open(args.target_path, 'w') as f: 
        f.write('source_id,target_id,count\n')
        for triple in triples:
            f.write('{},{},{}\n'.format(*triple))
