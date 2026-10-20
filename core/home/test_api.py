# import requests

# url = "http://127.0.0.1:8000/api/job/"

# payload = {
#     "title": "Python Developer Intern",
#     "company": "Example Nepal",
#     "location": "Itahari",
#     "description": "Work on backend APIs.",
#     "skills": ["Python", "Django"],
# }

# response = requests.post(url, json=payload)

# print(response.status_code)
# print(response.json())

# import requests

# url = "http://127.0.0.1:8000/api/job/"

# payload = {
#     "title": "Python Developer Intern",
#     "company": "Example Nepal",
#     "location": "Itahari",
#     "description": "Work on backend APIs.",
#     "skills": ["Python", "Django"],
# }

# response = requests.post(
#     url,
#     json=payload,
#     auth=("", ""),
# )

# print(response.status_code)
# print(response.json())


import requests
import uuid

url = "http://127.0.0.1:8000/api/auth/register/"
username = f"jobseeker_{uuid.uuid4().hex[:8]}"

payload = {
    "username": username,
    "email": f"{username}@example.com",
    "password": "DevOnlyPass123!",
    "role": "job_seeker",
}

response = requests.post(url, json=payload)

print("Status:", response.status_code)
try:
    print("Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Response body:", response.text)
