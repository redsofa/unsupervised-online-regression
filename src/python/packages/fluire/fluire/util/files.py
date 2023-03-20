from pathlib import Path


def mkdir_structure(fqn):
    p = Path(fqn)
    p.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    pass
