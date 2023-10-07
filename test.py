import requests
import json

data = {
    "rd":10,
    "fd":12
}

link_local = "http://localhost:80/upload/missionGuide/0.8.1.014.07/guide_test"
link_cloud = "http://60.204.171.248/upload/missionGuide/0.8.1.014.07/guide_test"
result = requests.post(link_cloud, json=data, verify=False, timeout=10)
print(result.content)