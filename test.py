import requests
import json

data = {
    "rd":10,
    "fd":12
}


result = requests.post("http://localhost:8688/upload/missionGuide/0.8.1.014.07/guide_test", json=data, verify=False, timeout=10)
print(result.content)