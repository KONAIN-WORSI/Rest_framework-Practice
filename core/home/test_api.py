
import requests

BASE_URL = "http://127.0.0.1:8000/api/job/"

payload = {
    "title": "Junior Django Developer Intern",
    "company": "Example Tech Nepal",
    "location": "Itahari",
    "description": "Work on Django and REST API development.",
    "skill": ["Python", "Django", "REST API", "SQL"],
}

response = requests.post(BASE_URL, json=payload)

print("HTTP status:", response.status_code)
print("Response:", response.json())
