from confluent_kafka import Producer
# from config_kafka import config

def callback(err, event):
    if err:
        print(f"Produce to topic {event.topic()} failed for event {event.key()}")
    else:
        val = event.value().decode("utf8")
        print(f"{val} sent to partition {event.partition()}")

def say_hello_key(producer, key, topic):

    value = f"Hello {key}"

    producer.produce(topic, value, key, on_delivery=callback)

def say_hello(producer, key, topic):

    value = f"Hello Word {key}"

    producer.produce(topic, value, on_delivery=callback)



if __name__=='__main__':

    config = {
    "bootstrap.servers":'localhost:9092,localhost:9093,localhost:9094',
    "security.protocol":"PLAINTEXT"
    }

    try :

        producer = Producer(config)

        print(f"connect {producer}")

        topic = "my_topic_3p_2r"

        keys = ['Stephane', 'Alexandre', 'Yasmine', 'Paul', 'Amy', 'Brenda', 'Cindy', 'Derrick', 'Elaine', 'Fred']


        #[say_hello(producer=producer, key=key, topic=topic) for key in keys]

        [say_hello_key(producer=producer, key=f"{key}", topic=topic) for key in keys]
    
    except Exception as e:

        print(f"{e}")


