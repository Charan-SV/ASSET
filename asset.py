import csv
import requests
from requests.auth import HTTPBasicAuth

# Jira Assets API details
WORKSPACE_ID = "5fb28908-8665-41c5-9fb1-3e0893279b72"
API_URL_CREATE = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/object/create"
API_URL_AQL = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/object/aql?startAt=0&maxResults=100&includeAttributes=true"

# Your Atlassian credentials
EMAIL = "charanv@padahsolutions.com"
API_TOKEN = "TOKEN"

# ObjectTypeId for "Users"
OBJECT_TYPE_ID = "86"

# Attribute IDs from your schema
ATTRIBUTES = {
    "Name": "698",
    "User": "699",
    "Email": "700",
    "LicenseSkuld": "701",
    "LicenseName": "702"
}

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Step 1: Fetch existing users using AQL
def get_existing_users():
    existing = set()
    payload = {
        "qlQuery": "objectType = Users"
    }
    response = requests.post(API_URL_AQL, headers=HEADERS, auth=HTTPBasicAuth(EMAIL, API_TOKEN), json=payload)
    if response.status_code == 200:
        data = response.json()
        for obj in data.get("values", []):
            for attr in obj.get("attributes", []):
                if attr.get("objectTypeAttributeId") == ATTRIBUTES["Email"]:
                    email_val = attr.get("objectAttributeValues", [{}])[0].get("value")
                    if email_val:
                        existing.add(email_val.lower())
    else:
        print(f"❌ Failed to fetch existing users: {response.status_code}, {response.text}")
    return existing

existing_emails = get_existing_users()

# Step 2: Function to create user object
def create_user_object(row):
    if row["Email"].lower() in existing_emails:
        print(f"ℹ️ User with Email '{row['Email']}' already exists. Skipping creation.")
        return

    payload = {
        "objectTypeId": OBJECT_TYPE_ID,
        "attributes": [
            {"objectTypeAttributeId": ATTRIBUTES["Name"], "objectAttributeValues": [{"value": row["Name"]}]},
            {"objectTypeAttributeId": ATTRIBUTES["User"], "objectAttributeValues": [{"value": row["User"]}]},
            {"objectTypeAttributeId": ATTRIBUTES["Email"], "objectAttributeValues": [{"value": row["Email"]}]},
            {"objectTypeAttributeId": ATTRIBUTES["LicenseSkuld"], "objectAttributeValues": [{"value": row["LicenseSkuld"]}]},
            {"objectTypeAttributeId": ATTRIBUTES["LicenseName"], "objectAttributeValues": [{"value": row["LicenseName"]}]}
        ]
    }

    response = requests.post(API_URL_CREATE, headers=HEADERS, json=payload, auth=HTTPBasicAuth(EMAIL, API_TOKEN))
    if response.status_code == 201:
        print(f"✅ Created user object: {row['Name']}")
        existing_emails.add(row["Email"].lower())
    else:
        print(f"❌ Failed to create {row['Name']}: {response.status_code}, {response.text}")

# Step 3: Read CSV and create objects
with open("users.csv", newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        create_user_object(row)
