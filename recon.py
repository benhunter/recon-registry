import os
import requests
import base64


class HarborClient:
    def __init__(self, user, password, url):
        self.user = user
        self.password = password
        self.url = url

    def get_projects(self):
        projects_endpoint = f"{self.url}/api/v2.0/projects"
        b64_credential = base64.encodebytes(f'{self.user}:{self.password}'.encode()).decode().strip()
        headers = {
            "Authorization": f"Basic {b64_credential}"
        }
        response = requests.get(projects_endpoint, headers=headers, verify=False)

        print(response)
        print(dir(response))

        if response.status_code == 200:
            json = response.json()
            project_names = [project.get('name') for project in json]
            print(project_names)
            # print(response.json()[0].get('name'))
            # repositories = response.json().get('repositories', [])
            # print("Repositories:", repositories)
        else:
            raise Exception(f"Failed to get projects: {response.status_code}, {response.text}")

# def get_catalog():
#     catalog_endpoint = f"{registry_url}/v2/_catalog"
#     response = requests.get(catalog_endpoint, verify=False)
#
#     if response.status_code == 200:
#         repositories = response.json().get('repositories', [])
#         print("Repositories:", repositories)
#     else:
#         raise Exception(f"Failed to fetch repositories: {response.status_code}, {response.text}")


def main():
    # Get credentials and registry details from environment variables
    username = os.getenv('DOCKER_REGISTRY_USERNAME')
    password = os.getenv('DOCKER_REGISTRY_PASSWORD')
    registry_url = os.getenv('DOCKER_REGISTRY_URL')

    if not all([username, password, registry_url]):
        raise ValueError("Missing one or more environment variables: DOCKER_REGISTRY_USERNAME, DOCKER_REGISTRY_PASSWORD, DOCKER_REGISTRY_URL")

    client = HarborClient(username, password, registry_url)

    client.get_projects()


if __name__ == '__main__':
    main()
