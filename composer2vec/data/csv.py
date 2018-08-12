def composers(path):
    """Yield composer tuples from CSV."""
    with open(path, 'r') as f:
        next(f)  # Skip headers
        for composer_id, line in enumerate(f):
            yield (composer_id, *line.strip().split('|'))
