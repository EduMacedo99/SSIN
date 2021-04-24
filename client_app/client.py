import requests
response = requests.get("http://127.0.0.1:3000/auth")
print(response)
print(response.json())  # This method is convenient when the API returns JSON
