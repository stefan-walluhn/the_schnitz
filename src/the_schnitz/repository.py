from the_schnitz.schema import LocationSchema


class RedisRepository:
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
