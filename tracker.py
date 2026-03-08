import requests
import sqlite3
import json
from datetime import datetime, UTC

CONFIG = json.load(open("config.json"))

TOKEN = CONFIG["token"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

DB = sqlite3.connect("db.sqlite")
CURSOR = DB.cursor()

# ---------- DB SETUP ----------

CURSOR.execute("""
CREATE TABLE IF NOT EXISTS repos(
id INTEGER PRIMARY KEY,
name TEXT,
owner TEXT
)
""")

CURSOR.execute("""
CREATE TABLE IF NOT EXISTS views(
repo TEXT,
date TEXT,
count INTEGER,
uniques INTEGER
)
""")

CURSOR.execute("""
CREATE TABLE IF NOT EXISTS clones(
repo TEXT,
date TEXT,
count INTEGER,
uniques INTEGER
)
""")

CURSOR.execute("""
CREATE TABLE IF NOT EXISTS referrers(
repo TEXT,
referrer TEXT,
count INTEGER,
uniques INTEGER,
date TEXT
)
""")

CURSOR.execute("""
CREATE TABLE IF NOT EXISTS paths(
repo TEXT,
path TEXT,
count INTEGER,
uniques INTEGER,
date TEXT
)
""")

DB.commit()

# ---------- FETCH REPOS ----------

def get_repos():

    repos = []
    page = 1

    while True:

        url = f"https://api.github.com/user/repos?per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS).json()

        if not r:
            break

        repos.extend(r)
        page += 1

    return repos


# ---------- TRAFFIC ----------

def get_views(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/traffic/views"
    return requests.get(url, headers=HEADERS).json()


def get_clones(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/traffic/clones"
    return requests.get(url, headers=HEADERS).json()


def get_referrers(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/traffic/popular/referrers"
    return requests.get(url, headers=HEADERS).json()


def get_paths(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/traffic/popular/paths"
    return requests.get(url, headers=HEADERS).json()


# ---------- SAVE ----------

def save_views(repo, data):

    for v in data.get("views", []):

        CURSOR.execute(
            "INSERT INTO views VALUES(?,?,?,?)",
            (repo, v["timestamp"], v["count"], v["uniques"])
        )


def save_clones(repo, data):

    for c in data.get("clones", []):

        CURSOR.execute(
            "INSERT INTO clones VALUES(?,?,?,?)",
            (repo, c["timestamp"], c["count"], c["uniques"])
        )


def save_referrers(repo, data):

    for r in data:

        CURSOR.execute(
            "INSERT INTO referrers VALUES(?,?,?,?,?)",
            (
                repo,
                r["referrer"],
                r["count"],
                r["uniques"],
                datetime.now(UTC)
            )
        )


def save_paths(repo, data):

    for p in data:

        CURSOR.execute(
            "INSERT INTO paths VALUES(?,?,?,?,?)",
            (
                repo,
                p["path"],
                p["count"],
                p["uniques"],
                datetime.now(UTC)
            )
        )


# ---------- MAIN ----------

def main():

    repos = get_repos()

    print("Repos found:", len(repos))

    for r in repos:

        name = r["name"]
        owner = r["owner"]["login"]

        print(f"Tracking {owner}/{name}")

        CURSOR.execute(
            "INSERT OR IGNORE INTO repos VALUES(?,?,?)",
            (r["id"], name, owner)
        )

        views = get_views(owner, name)
        clones = get_clones(owner, name)
        referrers = get_referrers(owner, name)
        paths = get_paths(owner, name)

        save_views(name, views)
        save_clones(name, clones)
        save_referrers(name, referrers)
        save_paths(name, paths)

        DB.commit()


if __name__ == "__main__":
    main()