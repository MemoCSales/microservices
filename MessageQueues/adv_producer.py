import pika
import json
import time
from datetime import datetime

def create_message(order_id, product, quantity):
	return {
		"order_id": order_id,
		"product": product,
		"quantity": quantity,
		"timestamp": datetime.now().isoformat()
	}

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Delcare a durable queue
channel.queue_declare(queue='orders', durable=True)

# Send multiple messages
orders = [
	create_message(1, "Laptop", 2),
	create_message(2, "Phone", 1),
	create_message(3, "Tablet", 3),
]

for order in orders:
	message = json.dumps(order)
	channel.basic_publish(
		exchange='',
		routing_key='orders',
		body=message,
		properties=pika.BasicProperties(
			delivery_mode=2, # Make message persistent
			content_type='application/json'
		)
	)
	print(f" [x] Sent order {order['order_id']}")
	time.sleep(1) # Simulate some processing time

connection.close()