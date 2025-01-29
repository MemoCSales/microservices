from fastapi import FastAPI

app = FastAPI()

# Sample data: Orders database
orders = {
	1: {"order_id": 1, "item": "Laptop", "status": "Shipped"},
	2: {"order_id": 2, "item": "Phone", "status": "Processing"}
}

# Endpoint to get order details
@app.get("/orders/{order_id}")
def get_order(order_id: int):
	order = orders.get(order_id)
	if order:
		return {"success": True, "data": order}
	return {"success": False, "error": "Order not found"}

# Run servive: uvicorn order_service:app --reload