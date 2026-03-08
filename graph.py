import json

data = json.load(open("traffic.json"))

html = """

<!DOCTYPE html>
<html>
<head>

<title>GitHub Stats</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
background:#0d1117;
color:white;
font-family:Arial;
padding:40px;
}

h1{
text-align:center;
margin-bottom:40px;
}

.repo{
background:#161b22;
padding:20px;
margin-bottom:40px;
border-radius:8px;
}

.repo h2{
margin:0;
}

.repo p{
color:#8b949e;
}

canvas{
margin-top:20px;
}

</style>

</head>

<body>

<h1>GitHub Stats</h1>

"""

chart_id = 0

for repo in data:

    chart_id += 1

    views_dates = [v["timestamp"][:10] for v in repo["views"]]
    views_counts = [v["count"] for v in repo["views"]]

    clones_dates = [c["timestamp"][:10] for c in repo["clones"]]
    clones_counts = [c["count"] for c in repo["clones"]]

    html += f"""

<div class="repo">

<h2>{repo["name"]}</h2>

<p>{repo["description"]}</p>

<p>⭐ {repo["stars"]} | 🍴 {repo["forks"]}</p>

<canvas id="views{chart_id}" height="120"></canvas>
<canvas id="clones{chart_id}" height="120"></canvas>

</div>

<script>

new Chart(document.getElementById("views{chart_id}"), {{
type:"line",
data:{{
labels:{views_dates},
datasets:[{{
label:"Views",
data:{views_counts},
borderColor:"#58a6ff",
tension:0.3
}}]
}},
options:{{
plugins:{{
tooltip:{{enabled:true}}
}}
}}
}})

new Chart(document.getElementById("clones{chart_id}"), {{
type:"line",
data:{{
labels:{clones_dates},
datasets:[{{
label:"Clones",
data:{clones_counts},
borderColor:"#3fb950",
tension:0.3
}}]
}},
options:{{
plugins:{{
tooltip:{{enabled:true}}
}}
}}
}})

</script>

"""

html += "</body></html>"

open("dashboard.html","w",encoding="utf8").write(html)

print("Created dashboard.html")