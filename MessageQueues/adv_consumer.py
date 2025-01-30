import pika
import json
import time
import threading

import pika.exceptions

def process_message(message):
	"""Simulate background processing"""
	order = json.loads(message)
	time.sleep(2) # Simulate processing time
	return f"Processed order {order['order_id']}: {order['quantity']}x {order['product']}"

def callback(ch, method, properties, body):
	print(f" [x] Received: '{body.decode()}'")

	# Process message in background thread
	def background_process():
		try:
			result = process_message(body)
			print(f" [x] Done: {result}")
			ch.basic_ack(delivery_tag=method.delivery_tag)
		except Exception as e:
			print(f"Error processing message: {e}")
	
	thread = threading.Thread(target=background_process)
	thread.start()

def start_consumer(consumer_id):
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		channel = connection.channel()
		
		"""
		durable = True -> Makes the queue persisten across RabbitMQ server restarts
		Without it the messages would be lost if RabbitMQ crashes or restarts
		"""
		channel.queue_declare(queue='orders', durable=True)

		# Fair dispatch - don't give more than one message to a worker at a time
		# Worker only gets new message after finishing current one
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(
			queue='orders',
			on_message_callback=callback,
			auto_ack=False # Requires manual acknowledgment after message is processed. Without it: Messages could be lost if consumer crashes during processing
		)

		print(f" [*] Consumer {consumer_id} waiting for messages. To exit press CTRL + C")
		channel.start_consuming()
	except pika.exceptions.StreamLostError:
		print(f"Consumer {consumer_id} finished processing - no more messages")
	except Exception as e:
		print(f"Consumer {consumer_id} encountered error: {e}")
	finally:
		try:
			connection.close()
		except:
			pass

# Start multiple consumers
if __name__ == "__main__":
	num_consumers = 3
	consumers = []

	for i in range(num_consumers):
		consumer = threading.Thread(target=start_consumer, args=(i,))
		consumers.append(consumer)
		consumer.start()

	# Wait for all consumers
	for consumer in consumers:
		consumer.join()