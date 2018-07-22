import argparse
import itertools

import nltk

import data
import model


nltk.download('punkt')


_DEFAULT_WINDOW_SIZE = 32


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', nargs=1,
                        help='Path to training file')
                        
    parser.add_argument('--save', help='Path to save model')
    parser.add_argument('--save_vocab', help='Path to save vocab file')
    parser.add_argument('--load', help='Path to load model')
    parser.add_argument('--load_vocab', help='Path to load vocab file')

    args = parser.parse_args()


def _main():
    args = _parse_args()

    if args.train:
        tokens_by_composer_id = data.tokens_by_composer_id(args.path)
        num_composers = len(tokens_by_composer_id)

        vocab = vocab.Vocab()
        if args.load_vocab:
            vocab.load(args.load_vocab)
        else:
            all_tokens = list(itertools.chain.from_iterable(tokens_by_composer_id.values()))
            vocab.build(all_tokens)

            if args.save_vocab:
                vocab.save(args.save_vocab)

        token_ids_by_composer_id = {c: v.to_ids(t) for c, t in tokens_by_composer_id}

        all_data = data.batch(
                data.data_generator(
                    token_ids_by_composer_id,
                    _DEFAULT_WINDOW_SIZE,
                    vocab.size))

        m = model.Model(_DEFAULT_WINDOW_SIZE,
                        vocab.size,
                        num_composers)
        
        m.build()
        m.compile()

        m.train(all_data())

        if args.save:
            m.save(args.save)


if __name__ == '__main__':
    _main()
