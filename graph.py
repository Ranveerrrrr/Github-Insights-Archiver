import json

repos = json.load(open("traffic.json"))

html = f"""
<!DOCTYPE html>
<html>
<head>

<title>GitHub Stats</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body {{
background:#0d1117;
color:white;
font-family:Arial;
padding:40px;
}}

h1 {{
text-align:center;
margin-bottom:40px;
}}

.repo {{
background:#161b22;
margin-bottom:15px;
border-radius:8px;
}}

.repo-header {{
padding:15px;
cursor:pointer;
font-weight:bold;
border-bottom:1px solid #30363d;
}}

.repo-content {{
display:none;
padding:20px;
}}

.repo p {{
color:#8b949e;
}}

canvas {{
margin-top:20px;
}}

a {{
color:#58a6ff;
}}

</style>

</head>

<body>

<h1>GitHub Stats</h1>

<div id="repos"></div>

<script>

const repos = {json.dumps(repos)};

function toggle(id) {{
let el = document.getElementById(id);
el.style.display = el.style.display === "block" ? "none" : "block";
}}

function createDashboard() {{

let container = document.getElementById("repos");

repos.forEach((repo, index) => {{

let repoId = "repo"+index;
let chartId = "chart"+index;

let repoHTML = `
<div class="repo">

<div class="repo-header" onclick="toggle('${{repoId}}')">
${{repo.name}}
</div>

<div class="repo-content" id="${{repoId}}">

<p>${{repo.description || "No description"}}</p>

<p>⭐ ${{repo.stars}} | 🍴 ${{repo.forks}}</p>

<a href="${{repo.url}}" target="_blank">${{repo.url}}</a>

<canvas id="${{chartId}}" height="120"></canvas>

</div>

</div>
`;

container.innerHTML += repoHTML;

setTimeout(() => {{

let labels = repo.views.map(v => v.timestamp.substring(0,10));
let views = repo.views.map(v => v.count);
let clones = repo.clones.map(v => v.count);

new Chart(document.getElementById(chartId), {{

type: "line",

data: {{
labels: labels,
datasets: [

{{
label: "Views",
data: views,
borderColor: "#58a6ff",
tension:0.3
}},

{{
label: "Clones",
data: clones,
borderColor: "#3fb950",
tension:0.3
}}

]
}},

options: {{
interaction:{{
mode:"index",
intersect:false
}},
plugins:{{
tooltip:{{enabled:true}}
}},
scales:{{
y:{{beginAtZero:true}}
}}
}}

}})

}},100)

}})

}}

createDashboard();

</script>

</body>
</html>
"""

open("dashboard.html","w",encoding="utf8").write(html)

print("dashboard.html created")