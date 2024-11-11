import pika


rabbitmq_host = 'rabbitmq'
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))

item_types = {
    '1': 'shirt',
    '2': 'shoes',
    '3': 'cupon_code',
    '4': 'tour_ticket'
}

queue_names = {
    'shipping': 'shipping_queue',
    'inventory': 'inventory_queue',
    'email': 'email_queue',
    'purchase': 'purchase_queue'
}


def send_to_exchange(message: dict):
    channel = connection.channel()

    # declare an exchange
    channel.exchange_declare(exchange='main_exchange', exchange_type='topic')
    # id 1 will go to all queues
    # id 2 will go to all queues
    # id 3 will go to email and purchase
    # id 4 will go to email and purchase and inventory

    if message['item_id'] in ['1', '2']:
        routing_key = f"{queue_names['shipping']}.{queue_names['inventory']}.{queue_names['email']}.{queue_names['purchase']}"
    elif message['item_id'] == '3':
        routing_key = f"{queue_names['email']}.{queue_names['purchase']}"
    elif message['item_id'] == '4':
        routing_key = f"{queue_names['email']}.{queue_names['purchase']}.{queue_names['inventory']}"
    else:
        routing_key = f"{queue_names['shipping']}.{queue_names['inventory']}.{queue_names['email']}.{queue_names['purchase']}"


    channel.basic_publish(exchange='main_exchange',
                          routing_key=routing_key,
                          body=str(message))