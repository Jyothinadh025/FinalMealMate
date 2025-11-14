import requests

try:
    response = requests.get("https://api.razorpay.com/v1/orders")
    print("✅ Connected successfully! Status Code:", response.status_code)
except Exception as e:
    print("❌ Connection failed:", e)
