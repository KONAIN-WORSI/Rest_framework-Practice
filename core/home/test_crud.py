
import requests

BASE_URL = "http://127.0.0.1:8000/api/job/"


def response_json(action, response):
    if not response.ok:
        raise requests.HTTPError(
            f"{action} failed with HTTP {response.status_code}: {response.text[:500]}",
            response=response,
        )

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise RuntimeError(
            f"{action} returned a non-JSON response: {response.text[:500]}"
        ) from error


# 1. GET: list all jobs
response = requests.get(BASE_URL)
jobs = response_json("List jobs", response)
print("List:", response.status_code, jobs)

# 2. POST: create a temporary test job
payload = {
    "title": "API Test Intern",
    "company": "Test Company",
    "location": "Itahari",
    "description": "Temporary record for CRUD testing.",
    "skill": ["Python", "Django"],
}

response = requests.post(BASE_URL, json=payload)
created_job = response_json("Create job", response)
print("Create:", response.status_code, created_job)

job_id = created_job.get("id")
if job_id is None:
    raise ValueError("Create response did not include a job ID.")
detail_url = f"{BASE_URL}{job_id}/"

# 3. GET: retrieve this job
response = requests.get(detail_url)
retrieved_job = response_json("Retrieve job", response)
print("Retrieve:", response.status_code, retrieved_job)

# 4. PATCH: change only the location
response = requests.patch(
    detail_url,
    json={"location": "Kathmandu"},
)
patched_job = response_json("Patch job", response)
print("Patch:", response.status_code, patched_job)

# 5. PUT: replace all required writable fields
replacement = {
    "title": "Backend Developer Intern",
    "company": "Example Software Nepal",
    "location": "Biratnagar",
    "description": "Build and test backend APIs.",
    "skill": ["Python", "Django", "PostgreSQL"],
}
response = requests.put(detail_url, json=replacement)
replaced_job = response_json("Replace job", response)
print("Put:", response.status_code, replaced_job)

# 6. DELETE: remove the temporary job
response = requests.delete(detail_url)
print("Delete:", response.status_code)

# 7. Verify deletion
response = requests.get(detail_url)
print("After delete:", response.status_code)
if response.status_code != 404:
    raise RuntimeError(
        f"Expected HTTP 404 after deletion, got HTTP {response.status_code}: "
        f"{response.text[:500]}"
    )
