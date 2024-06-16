import os
import requests

# Get credentials and registry details from environment variables
username = os.getenv('DOCKER_REGISTRY_USERNAME')
password = os.getenv('DOCKER_REGISTRY_PASSWORD')
registry_url = os.getenv('DOCKER_REGISTRY_URL')
registry_service = os.getenv('DOCKER_REGISTRY_SERVICE')

if not all([username, password, registry_url, registry_service]):
    raise ValueError("Missing one or more environment variables: DOCKER_REGISTRY_USERNAME, DOCKER_REGISTRY_PASSWORD, DOCKER_REGISTRY_URL, DOCKER_REGISTRY_SERVICE")

# Obtain the bearer token
token_endpoint = f"{registry_url}/v2/token"
params = {
    "service": registry_service,
    "scope": "registry:catalog:*"
}

response = requests.get(token_endpoint, auth=(username, password), params=params, verify=False)

if response.status_code == 200:
    token = response.json().get('token')
    print("Bearer Token obtained successfully")
else:
    raise Exception(f"Failed to obtain token: {response.status_code}, {response.text}")

# Use the bearer token to list repositories
catalog_endpoint = f"{registry_url}/v2/_catalog"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(catalog_endpoint, headers=headers, verify=False)

if response.status_code == 200:
    repositories = response.json().get('repositories', [])
    print("Repositories:", repositories)
else:
    raise Exception(f"Failed to fetch repositories: {response.status_code}, {response.text}")
