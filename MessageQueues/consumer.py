import pika

# 1. Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Create queue (if it doesnt exist)
channel.queue_declare(queue='hello')


# 3. Define a function to know how to process messages
def callback(ch, method, properties, body):
	print(f" [x] Mensaje recibido: '{body.decode()}'")

# 4. Listen to queue 'hello'
channel.basic_consume(queue='hello',
					  auto_ack=True,
					  on_message_callback=callback)

print(f" [x] Esperando mensajes. Preciona Ctrl + C para salir.")
channel.start_consuming()