# GitHub Traffic Archiver
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)
![Tracker.py](https://img.shields.io/badge/Tracker.py-Analytics-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)
![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/Ranveerrrrr/Github-Insights-Archiver?style=for-the-badge)
![Languages](https://img.shields.io/github/languages/top/Ranveerrrrr/Github-Insights-Archiver?style=for-the-badge)
![Language Count](https://img.shields.io/github/languages/count/Ranveerrrrr/Github-Insights-Archiver?style=for-the-badge)
![License](https://img.shields.io/github/license/Ranveerrrrr/Github-Insights-Archiver?style=for-the-badge)

## Overview

A lightweight tool to archive GitHub repository traffic data beyond GitHub's 14-day limit. It continuously collects and stores data to build long-term analytics and provides a local dashboard with time-based filtering.

## Features

- ✓ Stores GitHub traffic beyond 14 days
- ✓ Tracks views and clones over time
- ✓ Preserves referrers and popular paths
- ✓ Time-range filtering ("time machine" dashboard)
- ✓ No external database required

## How It Works

1. A Python script fetches GitHub traffic data using the GitHub API
2. Data includes:
   - Views
   - Clones
   - Referrers
   - Popular Paths
3. Data is merged with existing history (no duplicates)
4. Snapshots are stored over time to build a history
5. The dashboard visualizes and filters this data

## Folder Structure

```text
github-insights-archiver/
|──tracker.py      <- Main Script
|──config.json     <- Github Token
|──Dashboard/
   |──index.html      <- Main Dashboard
   |──style.css       <- UI Style
   |──app.js          <- Data Logic
   |──data (traffic.json, snapshots.json,  referrers_history.json and paths_history.json)
```

## Setup

1. Install dependencies:

```bash
pip install requests
```

2. Create `config.json`:

```json
{
  "token": "YOUR_GITHUB_TOKEN"
}
```

## Usage

Run the tracker:

```bash
python tracker.py
```

The script will:
- Fetch latest data
- Merge with history
- Update data inside Dashboard/

To view dashboard:
- Serve Dashboard/ via Nginx or open index.html
- Use date filters to explore history

## Automation (Cron)

Run daily:

```bash
0 0 * * * python3 /path/to/tracker.py
```

Regular execution ensures no data loss

## Notes

- GitHub limits traffic to 14 days
- This tool builds a persistent history
- Referrers and paths are snapshot based (preserved over time)
- Dashboard supports time-range analysis

## Security

- NEVER push `config.json`
- Use `.gitignore` to ignore sensitive and generated files


