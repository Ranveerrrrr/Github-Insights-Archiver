import requests
import json

TOKEN = json.load(open("config.json"))["token"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

repos = requests.get(
    "https://api.github.com/user/repos?per_page=100",
    headers=HEADERS
).json()

all_data = []

for repo in repos:

    owner = repo["owner"]["login"]
    name = repo["name"]

    print("Tracking", owner+"/"+name)

    views = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/views",
        headers=HEADERS
    ).json()

    clones = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/clones",
        headers=HEADERS
    ).json()

    repo_data = {
        "name": name,
        "description": repo["description"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "url": repo["html_url"],
        "views": views.get("views", []),
        "clones": clones.get("clones", [])
    }

    all_data.append(repo_data)

with open("traffic.json","w") as f:
    json.dump(all_data, f, indent=2)

print("traffic.json generated")