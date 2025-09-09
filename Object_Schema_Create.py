import requests
from requests.auth import HTTPBasicAuth

# Jira Assets API details
WORKSPACE_ID = "5fb28908-8665-41c5-9fb1-3e0893279b72"

# Atlassian credentials
EMAIL = "charanv@padahsolutions.com"
API_TOKEN = "TOKEN"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Step 1: Get schema details
schema_name = input("Enter Object Schema name (max 10 chars): ").strip()
schema_key = input("Enter Schema Key: ").strip()

# Step 2: Create Object Schema
schema_url = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/objectschema/create"
schema_payload = {
    "name": schema_name,
    "objectSchemaKey": schema_key,
    "description": f"{schema_name} schema"
}

response = requests.post(schema_url, headers=HEADERS, auth=HTTPBasicAuth(EMAIL, API_TOKEN), json=schema_payload)
if response.status_code in [200, 201]:
    schema = response.json()
    schema_id = schema.get("id")
    print(f"✅ Object Schema created successfully! Schema ID: {schema_id}")
else:
    print(f"❌ Failed to create schema: {response.status_code}")
    print(response.text)
    exit(1)

# Step 3: Create Object Type 'Users'
object_type_url = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/objecttype/create"
object_type_payload = {
    "inherited": False,
    "abstractObjectType": False,
    "objectSchemaId": schema_id,
    "iconId": "3",  # Example: AD icon
    "name": "Users",
    "description": "User object type"
}

response = requests.post(object_type_url, headers=HEADERS, auth=HTTPBasicAuth(EMAIL, API_TOKEN), json=object_type_payload)
if response.status_code in [200, 201]:
    object_type = response.json()
    object_type_id = object_type.get("id")
    print(f"✅ Object Type 'Users' created successfully! Object Type ID: {object_type_id}")
else:
    print(f"❌ Failed to create object type: {response.status_code}")
    print(response.text)
    exit(1)

# Step 4: Fetch all attributes including default 'Name'
attrs_url = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/objecttype/{object_type_id}/attributes"
response = requests.get(attrs_url, headers=HEADERS, auth=HTTPBasicAuth(EMAIL, API_TOKEN))

attribute_ids = {}
if response.status_code == 200:
    attrs_list = response.json() if isinstance(response.json(), list) else response.json().get("values", [])
    for attr in attrs_list:
        attribute_ids[attr["name"]] = attr["id"]
        print(f"ℹ️ Attribute found: {attr['name']} (ID: {attr['id']})")
else:
    print(f"❌ Failed to fetch attributes: {response.status_code}")
    print(response.text)
    exit(1)

# Step 5: Create remaining attributes if not present
custom_attributes = ["User", "Email", "LicenseSkuld", "LicenseName"]
for attr_name in custom_attributes:
    if attr_name in attribute_ids:
        print(f"ℹ️ Attribute '{attr_name}' already exists. Using existing ID: {attribute_ids[attr_name]}")
        continue

    attr_url = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/objecttypeattribute/{object_type_id}"
    payload = {
        "name": attr_name,
        "type": "0",          # 0 = Text
        "defaultTypeId": "0"
    }
    response = requests.post(attr_url, headers=HEADERS, auth=HTTPBasicAuth(EMAIL, API_TOKEN), json=payload)
    if response.status_code in [200, 201]:
        attr = response.json()
        attribute_ids[attr_name] = attr.get("id")
        print(f"✅ Attribute '{attr_name}' created successfully! Attribute ID: {attr.get('id')}")
    else:
        print(f"❌ Failed to create attribute '{attr_name}': {response.status_code}")
        print(response.text)

# Step 6: Final Summary
print("\n===== SUMMARY =====")
print(f"Object Schema ID : {schema_id}")
print(f"Object Type ID   : {object_type_id}")
print("Attribute IDs    :")
for name, attr_id in attribute_ids.items():
    print(f"  {name}: {attr_id}")
