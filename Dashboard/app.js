let repos = [];
let chart = null;

fetch("../traffic.json")
.then(res => res.json())
.then(data => {

repos = data;

const repoList = document.getElementById("repoList");

repos.forEach((repo,index)=>{

const item=document.createElement("div");

item.className="repo-item";
item.innerText=repo.name;

item.onclick=()=>{

document.querySelectorAll(".repo-item").forEach(i=>i.classList.remove("active"));
item.classList.add("active");

loadRepo(index);

};

repoList.appendChild(item);

});

document.querySelector(".repo-item").classList.add("active");
loadRepo(0);

});

function loadRepo(index){

const repo=repos[index];

const repoInfo = document.getElementById("repoInfo");

repoInfo.innerHTML=`
<div class="repo-title">${repo.name}</div>
<div class="repo-desc">${repo.description || "No description"}</div>
<div class="repo-meta">⭐ ${repo.stars} | 🍴 ${repo.forks}</div>
<a class="repo-link" href="${repo.url}" target="_blank">${repo.url}</a>
`;

const labels=repo.views.map(v=>v.timestamp.substring(0,10));
const views=repo.views.map(v=>v.count);
const clones=repo.clones.map(v=>v.count);

const totalViews=views.reduce((a,b)=>a+b,0);
const totalClones=clones.reduce((a,b)=>a+b,0);

document.getElementById("totalViews").innerText=totalViews;
document.getElementById("totalClones").innerText=totalClones;

if(chart) chart.destroy();

chart=new Chart(document.getElementById("chart"),{

type:"line",

data:{
labels:labels,
datasets:[
{
label:"Views",
data:views,
borderColor:"#58a6ff",
tension:0.3
},
{
label:"Clones",
data:clones,
borderColor:"#3fb950",
tension:0.3
}
]
},

options:{
interaction:{mode:"index",intersect:false},
plugins:{tooltip:{enabled:true}},
scales:{y:{beginAtZero:true}}
}

});

const refTable=document.getElementById("refTable");

refTable.innerHTML=`
<tr>
<th>Site</th>
<th>Views</th>
<th>Unique Visitors</th>
</tr>
`;

repo.referrers.forEach(r=>{
refTable.innerHTML+=`
<tr>
<td>${r.referrer}</td>
<td>${r.count}</td>
<td>${r.uniques}</td>
</tr>
`;
});

const contentTable=document.getElementById("contentTable");

contentTable.innerHTML=`
<tr>
<th>Content</th>
<th>Views</th>
<th>Unique Visitors</th>
</tr>
`;

repo.paths.forEach(p=>{
contentTable.innerHTML+=`
<tr>
<td>${p.path}</td>
<td>${p.count}</td>
<td>${p.uniques}</td>
</tr>
`;
});

}