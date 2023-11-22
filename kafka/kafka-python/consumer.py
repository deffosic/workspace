from confluent_kafka import Consumer, KafkaException
from config import config

def set_consumer_configs(config):
    config['group.id'] = 'hello_group'
    config['auto.offset.reset'] = 'earliest'
    config['enable.auto.commit'] = False

def assignment_callback(consumer, partitions):
    for p in partitions:
        print(f'Assigned to {p.topic}, partition {p.partition}')

if __name__ == '__main__':
    config = {
    "bootstrap.servers":'localhost:9092,localhost:9093,localhost:9094',
    "security.protocol":"PLAINTEXT"
    }
    set_consumer_configs(config)
    consumer = Consumer(config)
    consumer.subscribe(['my_topic_3p_2r'], on_assign=assignment_callback)

    while True:
        event = consumer.poll(1.0)
        if event is None:
            continue
        if event.error():
            raise KafkaException(event.error())
        else:
            val = event.value().decode('utf8')
            partition = event.partition()
            print(f'Received: {val} from partition {partition}    ')
            # consumer.commit(event)