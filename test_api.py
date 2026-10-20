import os

from apify_client import ApifyClient

# Set APIFY_API_TOKEN in the environment before running this script.
api_token = os.environ.get("APIFY_API_TOKEN")
if not api_token:
    raise RuntimeError("Set the APIFY_API_TOKEN environment variable.")
client = ApifyClient(api_token)
# Prepare the Actor input
run_input = {
    "keyword": "developer",  # Search for jobs with this keyword
    "category": "IT & Telecommunication" # Optional: filter by category
}

# Run the Actor and wait for it to finish
run = client.actor("bareezh_codes/merojob-nepal-jobs-scraper").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
print(f"💾 Check your data here: https://console.apify.com/storage/datasets/{run.default_dataset_id}")
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"💼 {item.get('title')} at {item.get('employerName')}")
    print(f"📍 Location: {item.get('jobLocations')}")
    print(f"🛠️  Skills: {item.get('skills')}")
    print(f"🔗 URL: {item.get('url')}")
    print("-" * 40)