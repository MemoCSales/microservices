import grpc
import order_pb2
import order_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = order_pb2_grpc.OrderServiceStub(channel)
response = stub.GetOrder(order_pb2.OrderRequest(order_id=1))
print (response)