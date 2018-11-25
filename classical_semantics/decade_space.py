import argparse

from keras.callbacks import Callback, EarlyStopping, ModelCheckpoint
from keras.layers import Input, Dense
from keras.models import load_model, Model

import numpy as np
from scipy.spatial import distance
import tensorflow as tf

from data import csv, embeddings


DEFAULT_NUM_EPOCHS = 250


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('embeddings_path', help='Path to embeddings directory')

    parser.add_argument('--train', help='Pass a path to annotated composers CSV'
                                        'in order to train')

    parser.add_argument('--save', help='Path to save model')
    parser.add_argument('--save_period', 
                        type=int,
                        help='Save model every n epochs')
    parser.add_argument('--save_embeddings',
                        help='Path to save embeddings file')
    parser.add_argument('--save_embeddings_period',
                        type=int,
                        help='Save embeddings every n epochs')

    parser.add_argument('--load', help='Path to load model')

    parser.add_argument('--early_stopping_patience',
                        type=int,
                        help='Stop after no loss decrease for n epochs')

    parser.add_argument('--num_epochs',
                        default=100,
                        type=int,
                        help='Number of epochs to train for')

    return parser.parse_args()


def _distance_loss(y_true, y_pred):
#    return distance.cosine(y_true, y_pred)
    return tf.losses.cosine_distance(y_true, y_pred, axis=-1)


class DecadeSpaceModel(object):

    def __init__(self, embedding_size):
        self._embedding_size = embedding_size

        self._model = None

    def build(self):
        inputs = Input(shape=(self._embedding_size,))
        outputs = Dense(self._embedding_size,
                        activation=None,
                        use_bias=False)(inputs)
        self._model = Model(inputs, outputs)

    def compile(self):
        self._model.compile(optimizer='sgd', loss=_distance_loss)

    def train(self, x, y,
              epochs=DEFAULT_NUM_EPOCHS,
              early_stopping_patience=None,
              save_path=None, save_period=None,
              save_embeddings_path=None, save_embeddings_period=None):

        callbacks=[]
        if early_stopping_patience:
            callbacks.append(EarlyStopping(monitor='loss',
                                           patience=early_stopping_patience))
        if save_path and save_period:
            callbacks.append(ModelCheckpoint(save_path,
                                             period=save_period))

        if save_embeddings_path and save_embeddings_period:
            callbacks.append(_SaveTransformedEmbeddings(x,
                                                        save_embeddings_path,
                                                        save_embeddings_period))

        history = self._model.fit(x, y, callbacks=callbacks, epochs=epochs)
  
        return history

    def save(self, path):
        logger.info('Saving model to %s', path)
        self._model.save(path)

    def load(self, path):
        logger.info('Loading model from %s', path)
        self._model = load_model(path)


class _SaveTransformedEmbeddings(Callback):

    def __init__(self, x, path, period):
        self._x = x
        self.path = path
        self.period = period

    def on_epoch_end(self, epoch, logs=None):
        if epoch % self.period != 0:
            return

        path = self.path.format(epoch=epoch)
        embeddings = self.model.predict(x)
        _write_doc_embeddings(embeddings, path)


def _write_embeddings(embeddings, path):
    logger.info('Saving embeddings to %s', path)
    with h5py.File(path, 'w') as f:
        f.create_dataset('doc_embeddings', data=embeddings)


def main():
    args = _parse_args()

    all_embeddings = embeddings.load(args.embeddings_path)
    embedding_size = all_embeddings.shape[1]
    x = all_embeddings

    m = DecadeSpaceModel(embedding_size)

    if args.load:
        m.load(args.load) 
    else:
        m.build()
        m.compile()

    elapsed_epochs = 0

    if args.train:
        composers = csv.composers(args.train)
        composers_data = np.array([(c[0], c[2]) for c in composers], dtype=np.int32)
        composers_data[:, 1] = (composers_data[:, 1] - 1000) / 10
        y = composers_data[:, 1]

        history = m.train(
                x, y,
                epochs=args.num_epochs,
                early_stopping_patience=args.early_stopping_patience,
                save_path=args.save,
                save_period=args.save_period,
                save_embeddings_path=args.save_embeddings,
                save_embeddings_period=args.save_embeddings_period)

        elapsed_epochs = len(history.history['loss'])

    if args.save:
        m.save(args.save.format(epoch=elapsed_epochs))

    if args.save_embeddings:
        y_hat = m.predict(x)
        _write_embeddings(y_hat, args.save_embeddings.format(epoch=elapsed_epochs))


if __name__ == '__main__':
    main()
