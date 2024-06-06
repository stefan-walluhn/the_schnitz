import uuid
import yaml


def locations(fp):
    return dict(
        LOCATIONS={uuid.UUID(k): v for k, v in yaml.safe_load(fp).items()}
    )
