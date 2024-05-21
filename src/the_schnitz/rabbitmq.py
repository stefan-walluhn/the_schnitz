import pika


class RabbitMQProducer:
    def __init__(self, host, exchange):
        self.exchange = exchange

        connection = pika.BlockingConnection(pika.ConnectionParameters(host))

        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=self.exchange,
                                      exchange_type='fanout')

    def publish(self, data):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key="",
                                   body=data)


class RabbitMQConsumer:
    def __init__(self, host, exchange, queue, callback):
        self.callback = callback

        connection = pika.BlockingConnection(pika.ConnectionParameters(host))

        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type='fanout')

        self.channel.queue_declare(queue)
        self.channel.queue_bind(exchange=exchange, queue=queue)

        self.channel.basic_consume(queue=queue,
                                   on_message_callback=self.__callback__,
                                   auto_ack=True)

    def subscribe(self):
        self.channel.start_consuming()

    def __callback__(self, ch, method, properties, body):
        self.callback(body)
