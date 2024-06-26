import msgpack

from pika.exceptions import AMQPHeartbeatTimeout


class RabbitMQProducer:
    def __init__(self, channel, exchange):
        self.channel, self.exchange = channel, exchange

        self.channel.exchange_declare(exchange=self.exchange,
                                      exchange_type="fanout")

    def publish(self, data):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key="",
                                   body=msgpack.packb(data))


class RabbitMQConsumer:
    def __init__(self, channel, exchange, queue, callback, exclusive=False):
        self.callback, self.channel = callback, channel

        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type="fanout")

        self.channel.queue_declare(queue=queue, exclusive=exclusive)
        self.channel.queue_bind(exchange=exchange, queue=queue)

        self.channel.basic_consume(queue=queue,
                                   on_message_callback=self.__callback__,
                                   auto_ack=True)

    def subscribe(self):
        try:
            self.channel.start_consuming()
        except AMQPHeartbeatTimeout:
            return

    def __callback__(self, ch, method, properties, body):
        self.callback(msgpack.unpackb(body))
