import requests

response = requests.get("http://127.0.0.1:8000/orders/1")
print(response.json())

# curl -s "http://127.0.0.1:8000/orders/1" | python3 -m json.tool
