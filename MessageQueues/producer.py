import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

message = "Hola, este es un mensaje del productor!"
channel.basic_publish(exchange='',
					  routing_key='hello',
					  body=message)

print(f" [x] Mensaje enviado: '{message}'")

connection.close()