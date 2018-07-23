from keras.callbacks import EarlyStopping
from keras.layers import Average, Concatenate, Dense, Embedding, Input, Lambda
from keras.models import Model
from keras.optimizers import SGD
import tensorflow as tf


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Composer2VecModel(object):

    def __init__(self, window_size, vocab_size, num_composers):
        self._window_size = window_size
        self._vocab_size = vocab_size
        self._num_composers = num_composers

        self._model = None

    @property
    def composer_embeddings(self):
        return np.array(self._model.layers[2].get_weights()[0])

    def build(self):
        sequence_input = Input(shape=(self._window_size,))
        composer_input = Input(shape=(1,))
      
        embedded_sequence = Embedding(input_dim=self._vocab_size, output_dim=300, input_length=self._window_size)(sequence_input)
        embedded_composer = Embedding(input_dim=self._num_composers, output_dim=300, input_length=1)(composer_input)
      
        embedded = Concatenate(axis=1)([embedded_composer, embedded_sequence])
        split = Lambda(lambda t: tf.split(t, self._window_size + 1, axis=1))(embedded)
        averaged = Average()(split)
        squeezed = Lambda(lambda t: tf.squeeze(t, axis=1))(averaged)
      
        softmax = Dense(self._vocab_size, activation='softmax')(squeezed)
      
        self._model = Model(inputs=[composer_input, sequence_input], outputs=softmax)

    def compile(self, optimizer=None):
        if not optimizer:
            optimizer = SGD(lr=0.001, momentum=0.9, nesterov=True)

        self._model.compile(optimizer=optimizer,
                            loss='categorical_crossentropy',
                            metrics=['categorical_accuracy'])

    def train(self, generator, steps_per_epoch=10000, epochs=1000):
        history = self._model.fit_generator(
	    generator,
	    callbacks=[
		EarlyStopping(monitor='loss', patience=10)
	      ],
	    steps_per_epoch=steps_per_epoch,
	    epochs=epochs)
  
        return history

    def save(self, path):
        logger.info('Saving model to %s', path)
        self._model.save(path)
