let repos = [];
let originalRepos = [];
let snapshots = [];
let refHistory = [];
let pathsHistory = [];

let currentRepoIndex = 0;
let activeFilter = null;

window.viewsChart = null;
window.clonesChart = null;

Promise.all([
    fetch("traffic.json").then(r => r.json()),
    fetch("snapshots.json").then(r => r.json()).catch(() => []),
    fetch("referrers_history.json").then(r => r.json()).catch(() => []),
    fetch("paths_history.json").then(r => r.json()).catch(() => [])
])
.then(([trafficData, snapshotData, refData, pathData]) => {

    repos = trafficData;
    originalRepos = JSON.parse(JSON.stringify(trafficData));
    snapshots = snapshotData;
    refHistory = refData;
    pathsHistory = pathData;

    repos = repos.map(repo => {

        const latestRef = refHistory.filter(r => r.repo === repo.name).at(-1);
        repo.referrers = latestRef ? latestRef.data : [];

        const latestPath = pathsHistory.filter(p => p.repo === repo.name).at(-1);
        repo.paths = latestPath ? latestPath.data : [];

        repo.stars = repo.stars || 0;
        repo.forks = repo.forks || 0;
        repo.url = repo.url || "#";
        repo.description = repo.description || "No description";

        return repo;
    });

    const repoList = document.getElementById("repoList");

    repos.forEach((repo, index) => {
        const item = document.createElement("div");
        item.className = "repo-item";
        item.innerText = repo.name;

        item.onclick = () => {
            document.querySelectorAll(".repo-item").forEach(i => i.classList.remove("active"));
            item.classList.add("active");
            currentRepoIndex = index;
            loadRepo(index);
        };

        repoList.appendChild(item);
    });

    if (repos.length) {
        document.querySelector(".repo-item").classList.add("active");
        currentRepoIndex = 0;
        loadRepo(0);
    }

});

function loadRepo(index) {

    const repo = repos[index];
    if (!repo) return;

    const repoInfo = document.getElementById("repoInfo");

    repoInfo.innerHTML = `
    <div class="repo-title">${repo.name}</div>
    <div class="repo-desc">${repo.description}</div>
    <div class="repo-meta">⭐ ${repo.stars} | 🍴 ${repo.forks}</div>
    <a class="repo-link" href="${repo.url}" target="_blank">${repo.url}</a>
    `;

    // ===== APPLY FILTER TO VIEWS/CLONES =====
    let views = repo.views;
    let clones = repo.clones;

    if (activeFilter) {
        views = views.filter(v => {
            const d = new Date(v.timestamp);
            return d >= activeFilter.start && d <= activeFilter.end;
        });

        clones = clones.filter(c => {
            const d = new Date(c.timestamp);
            return d >= activeFilter.start && d <= activeFilter.end;
        });
    }

    const labels = views.map(v => {
        const d = new Date(v.timestamp);
        return `${d.getDate()}/${d.getMonth() + 1}`;
    });

    const viewCounts = views.map(v => v.count);
    const viewUniques = views.map(v => v.uniques);

    const cloneCounts = clones.map(c => c.count);
    const cloneUniques = clones.map(c => c.uniques);

    // ===== STATS =====
    const totalViews = viewCounts.reduce((a, b) => a + b, 0);
    const totalClones = cloneCounts.reduce((a, b) => a + b, 0);
    const uniqueViews = viewUniques.reduce((a, b) => a + b, 0);
    const uniqueClones = cloneUniques.reduce((a, b) => a + b, 0);

    document.getElementById("totalViews").innerText = totalViews;
    document.getElementById("totalClones").innerText = totalClones;
    document.getElementById("uniqueViews").innerText = uniqueViews;
    document.getElementById("uniqueClones").innerText = uniqueClones;

    if (window.viewsChart) window.viewsChart.destroy();
    if (window.clonesChart) window.clonesChart.destroy();

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
            legend: { labels: { color: "#c9d1d9" } },
            tooltip: { mode: 'index', intersect: false }
        },
        scales: {
            x: {
                ticks: { color: "#8b949e" },
                grid: { color: "rgba(255,255,255,0.05)" }
            },
            y: {
                ticks: { color: "#8b949e" },
                grid: { color: "rgba(255,255,255,0.05)" }
            }
        }
    };

    // ===== CHARTS (UNCHANGED) =====
    window.viewsChart = new Chart(document.getElementById("viewsChart"), {
        type: "line",
        data: {
            labels,
            datasets: [
                { label: "Views", data: viewCounts, borderColor: "#4cc2ff", borderWidth: 2, tension: 0.4 },
                { label: "Unique Views", data: viewUniques, borderColor: "#ff9f43", borderWidth: 2, tension: 0.4 }
            ]
        },
        options: commonOptions
    });

    window.clonesChart = new Chart(document.getElementById("clonesChart"), {
        type: "line",
        data: {
            labels,
            datasets: [
                { label: "Clones", data: cloneCounts, borderColor: "#2ecc71", borderWidth: 2, tension: 0.4 },
                { label: "Unique Clones", data: cloneUniques, borderColor: "#a78bfa", borderWidth: 2, tension: 0.4 }
            ]
        },
        options: commonOptions
    });

    // ===== REFERRERS (FIXED) =====
    let refData = repo.referrers;

    if (activeFilter) {
        const filtered = refHistory
            .filter(r => r.repo === repo.name)
            .filter(r => {
                const d = new Date(r.timestamp);
                return d >= activeFilter.start && d <= activeFilter.end;
            });

        const agg = {};

        filtered.forEach(day => {
            day.data.forEach(r => {
                if (!agg[r.referrer]) agg[r.referrer] = { count: 0, uniques: 0 };
                agg[r.referrer].count += r.count;
                agg[r.referrer].uniques += r.uniques;
            });
        });

        refData = Object.entries(agg).map(([ref, val]) => ({
            referrer: ref,
            count: val.count,
            uniques: val.uniques
        }));
    }

    const refTable = document.getElementById("refTable");

    if (refData.length) {
        refTable.innerHTML = `<tr><th>Source</th><th>Views</th><th>Unique Views</th></tr>`;
        refData.forEach(r => {
            refTable.innerHTML += `
            <tr>
                <td>${r.referrer}</td>
                <td>${r.count}</td>
                <td>${r.uniques}</td>
            </tr>`;
        });
    } else {
        refTable.innerHTML = `<tr><td colspan="3">No data available</td></tr>`;
    }

    // ===== PATHS (FIXED) =====
    let pathData = repo.paths;

    if (activeFilter) {
        const filtered = pathsHistory
            .filter(p => p.repo === repo.name)
            .filter(p => {
                const d = new Date(p.timestamp);
                return d >= activeFilter.start && d <= activeFilter.end;
            });

        const agg = {};

        filtered.forEach(day => {
            day.data.forEach(p => {
                if (!agg[p.path]) agg[p.path] = { count: 0, uniques: 0 };
                agg[p.path].count += p.count;
                agg[p.path].uniques += p.uniques;
            });
        });

        pathData = Object.entries(agg).map(([path, val]) => ({
            path,
            count: val.count,
            uniques: val.uniques
        }));
    }

    const contentTable = document.getElementById("contentTable");

    if (pathData.length) {
        contentTable.innerHTML = `<tr><th>Path</th><th>Views</th><th>Unique Views</th></tr>`;
        pathData.forEach(p => {
            contentTable.innerHTML += `
            <tr>
                <td>${p.path}</td>
                <td>${p.count}</td>
                <td>${p.uniques}</td>
            </tr>`;
        });
    } else {
        contentTable.innerHTML = `<tr><td colspan="3">No data available</td></tr>`;
    }
}

// ===== FILTER =====
function applyFilter() {
    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;

    if (!start || !end) {
        alert("Select both dates");
        return;
    }

    activeFilter = {
        start: new Date(start),
        end: new Date(end)
    };

    loadRepo(currentRepoIndex);
}

// ===== RESET =====
function resetFilter() {
    document.getElementById("startDate").value = "";
    document.getElementById("endDate").value = "";

    activeFilter = null;
    loadRepo(currentRepoIndex);
}
