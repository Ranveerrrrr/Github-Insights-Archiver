import sqlite3
import json
from datetime import datetime

repo = "Discord-Music-Bot"

db = sqlite3.connect("db.sqlite")
cursor = db.cursor()

cursor.execute("""
SELECT date, count
FROM clones
WHERE repo=?
ORDER BY date
""", (repo,))

data = cursor.fetchall()

dates = []
counts = []

for d in data:
    dt = datetime.fromisoformat(d[0].replace("Z",""))
    dates.append(f"{dt.day}-{dt.month}-{dt.year%100}")
    counts.append(d[1])

with open("data.json","w") as f:
    json.dump({
        "dates": dates,
        "counts": counts
    }, f)