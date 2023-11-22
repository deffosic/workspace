from uuid import uuid4
import os

import protobuf.user_pb2 as user_pb2
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from config import config, sr_config



class User(object):

    def __init__(self, name, address, favorite_number, favorite_color):
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color
        # address should not be serialized, see user_to_dict()
        self._address = address


def user_to_dict(user, ctx):

    return dict(name=user.name,
                favorite_number=user.favorite_number,
                favorite_color=user.favorite_color)


def delivery_report(err, msg):

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))
    



if __name__ == '__main__':

    topic = "user_topic"
    

    schema_registry_client = SchemaRegistryClient(sr_config)

    string_serializer = StringSerializer('utf8')
    protobuf_serializer = ProtobufSerializer(user_pb2.User,
                                             schema_registry_client,
                                             {'use.deprecated.format': False})
    
    producer = Producer(config)


    print("Producing user records to topic {}. ^C to exit.".format(topic))

    while True:

        producer.poll(0.0)
        try:
            user_name = input("Enter name: ")
            user_favorite_number = int(input("Enter favorite number: "))
            user_favorite_color = input("Enter favorite color: ")
            user = user_pb2.User(name=user_name,
                                 favorite_color=user_favorite_color,
                                 favorite_number=user_favorite_number)
            producer.produce(topic=topic, partition=0,
                             key=string_serializer(str(uuid4())),
                             value=protobuf_serializer(user, SerializationContext(topic, MessageField.VALUE)),
                             on_delivery=delivery_report)
        except (KeyboardInterrupt, EOFError):
            break
        except ValueError:
            print("Invalid input, discarding record...")
            continue

    producer.flush()




