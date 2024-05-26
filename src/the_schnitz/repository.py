from abc import ABCMeta, abstractmethod
from the_schnitz.schema import LocationSchema


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def find_location(self, id):
         ...

    @abstractmethod
    def upsert_location(self, location):
        ...


class ConfigRepository(Repository):
    def __init__(self, location_data):
        self.location_data = location_data
        self.schema = LocationSchema()

    def find_location(self, id):
        data = self.location_data.get(id, None)
        if not data:
            return None

        return self.schema.load({'id': id} | data)

    def upsert_location(self, location):
        raise NotImplementedError('changing config is not implemented')


class RedisRepository(Repository):
    def __init__(self, client):
        self.client = client
        self.schema = LocationSchema(load_only=('id',))

    def find_location(self, id):
        data = self.client.hgetall(str(id))
        if not data:
            return None

        return self.schema.load({'id': id} | data)

    def upsert_location(self, location):
        self.client.hset(str(location.id), mapping=self.schema.dump(location))
