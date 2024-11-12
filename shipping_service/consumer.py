import pika
import pymongo
import json
import os
import time
import logging

logging.basicConfig(level=logging.DEBUG)

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
mongo_host = os.environ.get('MONGO_HOST', 'db-mongo')


def connect_mongo():
    while True:
        try:
            client = pymongo.MongoClient(host=mongo_host, port=27017, serverSelectionTimeoutMS=5000)
            client.admin.command('ismaster')
            print("Connected to MongoDB")
            return client
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(f"MongoDB connection error: {err}")
            time.sleep(5)

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            print("Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError as err:
            print(f"RabbitMQ connection error: {err}")
            time.sleep(5)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f" [x] Received {data}")
    # save the data
    collection.insert_one(data)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    global collection

    client = connect_mongo()
    db = client['shipping_db']
    collection = db['shipping']

    connection = connect_rabbitmq()
    channel = connection.channel()
    channel.exchange_declare(exchange='main_exchange', exchange_type='topic')

    channel.queue_declare(queue='shipping_queue', durable=True)
    channel.queue_bind(exchange='main_exchange', queue='shipping_queue', routing_key='shipping')

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='shipping_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()
