import requests
import json
import os
import time
from datetime import datetime

BASE_DIR = "Dashboard"
os.makedirs(BASE_DIR, exist_ok=True)

CONFIG_FILE = "config.json"
OUTPUT_FILE = f"{BASE_DIR}/traffic.json"
SNAPSHOT_FILE = f"{BASE_DIR}/snapshots.json"
REFERRER_HISTORY_FILE = f"{BASE_DIR}/referrers_history.json"
PATHS_HISTORY_FILE = f"{BASE_DIR}/paths_history.json"
STARS_FILE = f"{BASE_DIR}/stars.json"

# ------------------ LOAD TOKEN ------------------
with open(CONFIG_FILE, "r") as f:
    TOKEN = json.load(f)["token"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

STAR_HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3.star+json"
}

# ------------------ HELPERS ------------------
def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def safe_get(url, headers):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return {}

# ------------------ LOAD DATA ------------------
old_data = load_json(OUTPUT_FILE, [])
snapshots = load_json(SNAPSHOT_FILE, [])
ref_history = load_json(REFERRER_HISTORY_FILE, [])
paths_history = load_json(PATHS_HISTORY_FILE, [])
stars_data = load_json(STARS_FILE, {})

old_data_map = {repo["name"]: repo for repo in old_data}
all_data = []

# Dedup sets
snapshot_keys = {(s["repo"], s["timestamp"]) for s in snapshots}
ref_keys = {(r["repo"], r["timestamp"]) for r in ref_history}
path_keys = {(p["repo"], p["timestamp"]) for p in paths_history}

# ------------------ FETCH REPOS ------------------
repos = safe_get(
    "https://api.github.com/user/repos?per_page=100",
    HEADERS
)

# ------------------ PROCESS ------------------
for repo in repos:
    owner = repo["owner"]["login"]
    name = repo["name"]

    print(f"[+] Tracking {owner}/{name}")

    views = safe_get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/views",
        HEADERS
    )

    clones = safe_get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/clones",
        HEADERS
    )

    referrers = safe_get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/popular/referrers",
        HEADERS
    )

    paths = safe_get(
        f"https://api.github.com/repos/{owner}/{name}/traffic/popular/paths",
        HEADERS
    )

    now = datetime.utcnow().replace(microsecond=0).isoformat()

    # ------------------ CLEAN REFERRERS ------------------
    clean_referrers = []
    for r in referrers if isinstance(referrers, list) else []:
        clean_referrers.append({
            "referrer": r.get("referrer"),
            "count": r.get("count", 0),
            "uniques": r.get("uniques", 0)
        })

    # ------------------ CLEAN PATHS ------------------
    clean_paths = []
    for p in paths if isinstance(paths, list) else []:
        clean_paths.append({
            "path": p.get("path"),
            "count": p.get("count", 0),
            "uniques": p.get("uniques", 0)
        })

    # ------------------ MERGE TRAFFIC ------------------
    repo_data = {
        "name": name,
        "views": views.get("views", []),
        "clones": clones.get("clones", [])
    }

    if name in old_data_map:
        existing = old_data_map[name]

        existing_views = {v["timestamp"]: v for v in existing.get("views", [])}
        for v in repo_data["views"]:
            existing_views[v["timestamp"]] = v

        existing_clones = {c["timestamp"]: c for c in existing.get("clones", [])}
        for c in repo_data["clones"]:
            existing_clones[c["timestamp"]] = c

        existing["views"] = sorted(existing_views.values(), key=lambda x: x["timestamp"])
        existing["clones"] = sorted(existing_clones.values(), key=lambda x: x["timestamp"])

        all_data.append(existing)
    else:
        all_data.append(repo_data)

    # ------------------ SNAPSHOT ------------------
    if (name, now) not in snapshot_keys:
        snapshots.append({
            "repo": name,
            "timestamp": now,
            "total_views": views.get("count", 0),
            "total_clones": clones.get("count", 0),
            "unique_views": views.get("uniques", 0),
            "unique_clones": clones.get("uniques", 0),
            "stars": repo.get("stargazers_count"),
            "forks": repo.get("forks_count")
        })
        snapshot_keys.add((name, now))

    # ------------------ REF HISTORY ------------------
    if (name, now) not in ref_keys:
        ref_history.append({
            "repo": name,
            "timestamp": now,
            "data": clean_referrers
        })
        ref_keys.add((name, now))

    # ------------------ PATH HISTORY ------------------
    if (name, now) not in path_keys:
        paths_history.append({
            "repo": name,
            "timestamp": now,
            "data": clean_paths
        })
        path_keys.add((name, now))

    # ------------------ STARS ------------------
    if name not in stars_data:
        stars_data[name] = []

    existing_star_set = {
        (s["user"], s["starred_at"]) for s in stars_data[name]
    }

    page = 1
    max_pages = 10

    while page <= max_pages:
        res = safe_get(
            f"https://api.github.com/repos/{owner}/{name}/stargazers?per_page=100&page={page}",
            STAR_HEADERS
        )

        if not res or isinstance(res, dict):
            break

        for star in res:
            entry = (
                star.get("user", {}).get("login"),
                star.get("starred_at")
            )

            if entry not in existing_star_set:
                stars_data[name].append({
                    "user": entry[0],
                    "starred_at": entry[1]
                })
                existing_star_set.add(entry)

        page += 1

    time.sleep(1)

# ------------------ SAVE ------------------
save_json(OUTPUT_FILE, all_data)
save_json(SNAPSHOT_FILE, snapshots)
save_json(REFERRER_HISTORY_FILE, ref_history)
save_json(PATHS_HISTORY_FILE, paths_history)
save_json(STARS_FILE, stars_data)

print("\n[✔] CLEAN analytics dataset updated")

# ------------------ HEALTHCHECK ------------------
try:
    requests.get("https://hc-ping.com/0e103d7d-2736-4001-82fa-73756dd225f7", timeout=5)
except:
    pass
