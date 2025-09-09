import csv
import requests
from requests.auth import HTTPBasicAuth

# Jira Assets API details
WORKSPACE_ID = "5fb28908-8665-41c5-9fb1-3e0893279b72"
API_URL = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/object/create"

# Your Atlassian credentials
EMAIL = "charanv@padahsolutions.com"
API_TOKEN = "ATATT3xFfGF0_4V7B6FHMql6BjsgOodPLE7a32nGi56k5YQJAwANPsyH6KYrJ6khqsXKINLUuptc8F8bDuHDPvWMODBGPnUzS4UEDxm8P5BGdOweD6NFVs_8lF5ef9iTifjlzYPWDpspotf_YvpOSQ4vI38qQT_xtQN67TYTt5a4HGV-pXaXegQ=8EF33B87"

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

# Headers (no Authorization here, handled by HTTPBasicAuth)
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def create_user_object(row):
    payload = {
        "objectTypeId": OBJECT_TYPE_ID,
        "attributes": [
            {
                "objectTypeAttributeId": ATTRIBUTES["Name"],
                "objectAttributeValues": [{"value": row["Name"]}]
            },
            {
                "objectTypeAttributeId": ATTRIBUTES["User"],
                "objectAttributeValues": [{"value": row["User"]}]
            },
            {
                "objectTypeAttributeId": ATTRIBUTES["Email"],
                "objectAttributeValues": [{"value": row["Email"]}]
            },
            {
                "objectTypeAttributeId": ATTRIBUTES["LicenseSkuld"],
                "objectAttributeValues": [{"value": row["LicenseSkuld"]}]
            },
            {
                "objectTypeAttributeId": ATTRIBUTES["LicenseName"],
                "objectAttributeValues": [{"value": row["LicenseName"]}]
            }
        ]
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    if response.status_code == 201:
        print(f"✅ Created user object: {row['Name']}")
    else:
        print(f"❌ Failed to create {row['Name']}: {response.status_code}, {response.text}")

# Read CSV and create objects
with open("users.csv", newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        create_user_object(row)
