import grpc
from concurrent import futures
import order_pb2
import order_pb2_grpc
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys

class OrderService(order_pb2_grpc.OrderServiceServicer):
	def GetOrder(self, request, context):
		return order_pb2.OrderResponse(order_id=request.order_id, status="Shipped")

class ServerReloader(FileSystemEventHandler):
	def on_modified(self, event):
		if event.src_path.endswith('.py'):
			print(f"Code change detected. Restarting...")
			os.execv(sys.executable, ['python'] + sys.argv)

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
	server.add_insecure_port("[::]:50051")
	server.start()

	observer = Observer()
	observer.schedule(ServerReloader(), path='.', recursive=False)
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
		server.stop(0)
	observer.join()

if __name__ == '__main__':
	serve()


"""
Generate the gRPC code:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. order.proto

Run the server:
python order_service.py

Run the client:
python client.py
"""