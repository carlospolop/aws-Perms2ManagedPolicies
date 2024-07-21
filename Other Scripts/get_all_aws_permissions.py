import requests

# URL of the JSON file
url = 'https://raw.githubusercontent.com/iann0036/iam-dataset/main/aws/iam_definition.json'

def fetch_permissions(url):
    # Download the JSON data from the URL
    response = requests.get(url)
    data = response.json()
    # Initialize a list to store the permissions
    permissions = []
    # Loop through each service and their privileges
    for service in data:
        prefix = service['prefix']
        for privilege in service['privileges']:
            permission = f"{prefix}:{privilege['privilege']}"
            permissions.append(permission)
    return permissions

# Fetch permissions and print them
permissions_list = fetch_permissions(url)
print(permissions_list)