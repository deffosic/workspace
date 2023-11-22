from confluent_kafka.admin import (AdminClient, NewTopic, ConfigResource)
from config import config


def topic_exists(admin, topic):
    metadata = admin.list_topics()
    for t in iter(metadata.topics.values()):
        if t.topic == topic:
            return True
    return False

def create_topic(admin, topic, num_partition=6, replicat=1):
    new_topic = NewTopic(topic, num_partitions=num_partition, replication_factor=replicat) 
    result_dict = admin.create_topics([new_topic])
    for topic, future in result_dict.items():
        try:
            future.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))

def get_max_size(admin, topic):
    resource = ConfigResource('topic', topic)
    result_dict = admin.describe_configs([resource])
    config_entries = result_dict[resource].result()
    max_size = config_entries['max.message.bytes']
    return max_size.value

def set_max_size(admin, topic, max_k):
    config_dict = {'max.message.bytes': str(max_k*1024)}
    resource = ConfigResource('topic', topic, config_dict)
    result_dict = admin.alter_configs([resource])
    result_dict[resource].result()

if __name__ == '__main__':

    config = {
    "bootstrap.servers":'localhost:9092,localhost:9093,localhost:9094',
    "security.protocol":"PLAINTEXT"
    }

    admin = AdminClient(config)
    topic_name = 'my_topic_3p_2r'
    max_msg_k = 50

    if not topic_exists(admin, topic_name):
        create_topic(admin, topic_name, num_partition=3, replicat=2)

    current_max = get_max_size(admin, topic_name)
    if current_max != str(max_msg_k * 1024):
        print(f'Topic, {topic_name} max.message.bytes is {current_max}.')
        set_max_size(admin, topic_name, max_msg_k)

    new_max = get_max_size(admin, topic_name)
    print(f'Now max.message.bytes for topic {topic_name} is {new_max}')





