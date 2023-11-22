import protobuf.user_pb2 as user_pb2

from six.moves import input
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from config import config

def set_consumer_configs():
    config['group.id'] = 'hello_group'
    config['auto.offset.reset'] = 'earliest'
    config['enable.auto.commit'] = False


if __name__ == '__main__':

    topic = args.topic

    set_consumer_config()

    protobuf_deserializer = ProtobufDeserializer(user_pb2.User,
                                                 {'use.deprecated.format': False})

    consumer_conf = {'bootstrap.servers': args.bootstrap_servers,
                     'group.id': args.group,
                     'auto.offset.reset': "earliest"}

    consumer = Consumer(config)
    consumer.subscribe([topic])

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            user = protobuf_deserializer(msg.value(), SerializationContext(topic, MessageField.VALUE))

            if user is not None:
                print("User record {}:\n"
                      "\tname: {}\n"
                      "\tfavorite_number: {}\n"
                      "\tfavorite_color: {}\n"
                      .format(msg.key(), user.name,
                              user.favorite_number,
                              user.favorite_color))
        except KeyboardInterrupt:
            break

    consumer.close()
