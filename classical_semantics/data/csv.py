import pandas as pd


def composers(path):
    """Yield composer tuples from CSV."""
    with open(path, 'r') as f:
        next(f)  # Skip headers
        for composer_id, line in enumerate(f):
            yield (composer_id, *line.strip().split('|'))


def links(path):
    """Return Wikipedia link graph from CSV.
    
    Will return a dict of source composer id to a list of target
    composer ids, in descending order of frequency.
    """
    df = pd.read_csv(path)
    source_id_to_target_ids = {s_id: group['target_id'].tolist()
                               for s_id, group
                               in df.groupby('source_id')}

    return source_id_to_target_ids
