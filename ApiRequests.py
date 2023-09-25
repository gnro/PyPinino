import requests

# Define the URL you want to request
class carCapas:
    def __init__(self, url):
        url = "http://192.168.1.147:8080/api/sparkle/"
        self.url = url
    
    def consumeGet(self,endPoint):
        try:
            response = requests.get(self.url+endPoint)
            if response.status_code == 200:
                data = response.json()
                return (data)
            else:
                print(f"Request failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
    
    def consumePost(self, endPoint, data):
        try:
            response = requests.post(self.url+endPoint, json=data)
            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                print(f"Request failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
    