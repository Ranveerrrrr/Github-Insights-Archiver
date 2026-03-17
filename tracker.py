import requests
import json
import os
import time

CONFIG_FILE = "config.json"
OUTPUT_FILE = "traffic.json"

# ------------------ LOAD TOKEN ------------------
with open(CONFIG_FILE, "r") as f:
    TOKEN = json.load(f)["token"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ------------------ LOAD OLD DATA ------------------
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r") as f:
        old_data = json.load(f)
else:
    old_data = []

# Convert old data into dict for fast lookup
old_data_map = {repo["name"]: repo for repo in old_data}

all_data = []

# ------------------ FETCH REPOS ------------------
repos = requests.get(
    "https://api.github.com/user/repos?per_page=100",
    headers=HEADERS
).json()

# ------------------ PROCESS EACH REPO ------------------
for repo in repos:
    owner = repo["owner"]["login"]
    name = repo["name"]

    print(f"[+] Tracking {owner}/{name}")

    # Fetch traffic data
    views = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/views",
        headers=HEADERS
    ).json()

    clones = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/clones",
        headers=HEADERS
    ).json()

    referrers = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/popular/referrers",
        headers=HEADERS
    ).json()

    paths = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/popular/paths",
        headers=HEADERS
    ).json()

    # ------------------ NEW DATA STRUCTURE ------------------
    repo_data = {
        "name": name,
        "description": repo.get("description"),
        "stars": repo.get("stargazers_count"),
        "forks": repo.get("forks_count"),
        "url": repo.get("html_url"),
        "views": views.get("views", []),
        "clones": clones.get("clones", []),
        "referrers": referrers,
        "paths": paths
    }

    # ------------------ MERGE LOGIC ------------------
    if name in old_data_map:
        existing = old_data_map[name]

        # Merge views
        existing_views = {
            v["timestamp"]: v for v in existing.get("views", [])
        }
        for v in repo_data["views"]:
            existing_views[v["timestamp"]] = v

        # Merge clones
        existing_clones = {
            c["timestamp"]: c for c in existing.get("clones", [])
        }
        for c in repo_data["clones"]:
            existing_clones[c["timestamp"]] = c

        # Update merged data
        existing["views"] = list(existing_views.values())
        existing["clones"] = list(existing_clones.values())

        # Update metadata
        existing["description"] = repo_data["description"]
        existing["stars"] = repo_data["stars"]
        existing["forks"] = repo_data["forks"]
        existing["url"] = repo_data["url"]
        existing["referrers"] = repo_data["referrers"]
        existing["paths"] = repo_data["paths"]

        all_data.append(existing)

    else:
        # New repo
        all_data.append(repo_data)

    # Avoid hitting rate limits
    time.sleep(1)

# ------------------ SAVE DATA ------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(all_data, f, indent=2)

print("\n[✔] traffic.json updated successfully")