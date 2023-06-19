import os
import requests
import subprocess

# GitHub API endpoint for listing organization repositories
API_URL = 'https://api.github.com/orgs/{organization}/repos'

# Replace with the organization name
organization = 'Microchip-MPLAB-Harmony'

# Replace with your desired local directory to clone the repositories into
clone_directory = os.getcwd()


# Make a GET request to the GitHub API to retrieve the organization repositories
response = requests.get(API_URL.format(organization=organization))

# Check if the API request was successful
if response.status_code == 200:
    repositories = response.json()

    # Check if there are more repositories and handle pagination
    while 'next' in response.links:
        response = requests.get(response.links['next']['url'])
        repositories.extend(response.json())

    # Get the number of repositories
    num_repos = len(repositories)
    print(f"There are {num_repos} repositories available to clone.")

    # Save repository names to a text file
    with open('repository_names.txt', 'w') as file:
        file.write(f"Number of repositories: {num_repos}\n")
        file.write("Repository names:\n")
        for repo in repositories:
            file.write(repo['name'] + '\n')

    # Prompt user for confirmation
    confirmation = input("Do you want to proceed and clone all repositories? (Y/N): ")

    if confirmation.upper() == 'Y':
        # Iterate over the repositories and clone each one
        for repo in repositories:
            repo_name = repo['name']
            repo_url = repo['clone_url']
            clone_path = os.path.join(os.getcwd(), repo_name)

            # Clone the repository using the git command-line tool
            subprocess.run(['git', 'clone', repo_url, clone_path])

        print("Repositories cloned successfully.")
    else:
        print("Cloning canceled.")
else:
    print('Failed to retrieve organization repositories. Status code:', response.status_code)
