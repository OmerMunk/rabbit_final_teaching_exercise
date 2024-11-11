import pika
import pymongo
import json

import logging
logging.basicConfig(level=logging.DEBUG)


client = pymongo.MongoClient('localhost', 27017)
db = client['shipping_db']
collection = db['shipping']


rabbitmq_host = 'rabbitmq'
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))



def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f" [x] Received {data}")
    # save the data
    collection.insert_one(data)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    channel = connection.channel()
    channel.exchange_declare(exchange='main_exchange', exchange_type='topic')

    channel.queue_declare(queue='shipping_queue', durable=True)
    channel.queue_bind(exchange='main_exchange', queue='shipping_queue', routing_key='shipping')

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='shipping_queue',on_message_callback=callback)


    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()