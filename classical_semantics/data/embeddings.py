import h5py


def load(path):
    with h5py.File(path, 'r') as f:
        return f.get('doc_embeddings').value
