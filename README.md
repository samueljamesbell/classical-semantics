# Classical semantics

A series of experiments in semantically-informed classical music
recommendation.

## Introduction
Music recommendation from services like Spotify works on the principle of
"listeners like you": people who listen to Hot Chip also tend to listen to LCD
Soundsystem, so the latter might be a good recommendation.

In classical music, this doesn't seem to cut it. Perhaps this is because the
signal of listeners who listen thematically is drowned out by the noise of
those who listen to the most famous few (Mozart, Beethoven, Bach, etc.) and no
further. Here *thematically* implies consistency along some lines, be they
chronological, geographic or otherwise. If you're listening to 20th Century
British composers, perhaps another 20th Century British composer might be a
good next choice. The same is true for Italian composers of the Renaissance,
German of the Romantic, and so on. 

To do a good job of this, we need some semantic understanding of a
composer: who they are, where they lived, and when they were active
are all pertinent questions. This repo contains a selection of
experiments in recommending similar composers based on such knowledge.

## Details
Wikipedia, helpfully, contains plenty of information about most composers. We
use [`doc2vec`](https://github.com/samueljamesbell/doc2vec) [1] to build
dense vector representations of composers from the information on their Wikipedia
page. This leaves us with a composer space, where similar composers are close
together, and dissimilar far apart.

There's no gold standard for composer similarity, so we evaluate against a
simple benchmark: we deem the most similar composer to be the one that is most
frequently linked-to from a given composer's Wikipedia page.

Note that `doc2vec` is an unsupervised approach. We don't train the model to
reproduce this benchmark, but only evaluate it after the fact, with pleasing
results.

## Notebooks
The following notebooks illustrate the results. They can be viewed and interacted with using [Binder](https://mybinder.org/v2/gh/samueljamesbell/classical-semantics/master).

You can also use the TensorFlow Projector to explore the embedding space,
[here](https://projector.tensorflow.org/?config=https://raw.githubusercontent.com/samueljamesbell/classical-semantics/master/projector_config.json).

1. `notebooks/playground.ipynb` will show the top 5 recommended composers for a
   given input name.
2. `notebooks/dm-v-dbow.ipynb` evaluates our trained
   models' outputs against the Wikipedia link-frequency benchmark, comparing
   the DM and DBOW algorithms.
4. `notebooks/similarity-examples-dbow.ipynb` shows the results for a few
   cherry-picked examples.
3. `notebooks/similarity-pairwise-dbow.ipynb` shows cherry-picked examples
   becoming closer or more distant in composer space over time, as training
   progresses.
4. `notebooks/similarity-matrices-dbow.ipynb` shows structure emerging in similarity
   matrices ordered by composer birth year, demonstrating that the model learns
   to group composers of similar eras.

## Datasets
* `data/composers.csv` is a CSV of ~3K composer names, birth and death years,
  and Wikipedia links.
* `data/wikipedia/` is a directory containing scraped Wikipedia pages for each
  of the above composers.
* `data/wikpedia-links.csv` is a CSV of composers that link to each other, and
  how many times, on Wikipedia.
* `data/embeddings/` is a directory containing our trained composer embeddings.

## References
1. Le, Quoc, and Tomas Mikolov. "Distributed representations of sentences and
   documents." International Conference on Machine Learning. 2014.
