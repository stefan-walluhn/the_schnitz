import uuid
import yaml


def load(fp):
    def load_yaml(fp):
        return yaml.safe_load(fp)

    return dict(
        LOCATIONS={uuid.UUID(k): v for k, v in load_yaml(fp).items()}
    )
