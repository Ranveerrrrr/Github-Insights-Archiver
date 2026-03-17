# GitHub Traffic Archiver
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)
![Tracker.py](https://img.shields.io/badge/Tracker.py-Analytics-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)
![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/Ranveerrrrr/Github-Insights-Archiver?style=for-the-badge)
![Languages](https://img.shields.io/github/languages/top/Ranveerrrrr/Github-Insights-Archiver?style=for-the-badge)
![Language Count](https://img.shields.io/github/languages/count/Ranveerrrrr/Github-Insights-Archiver?style=for-the-badge)

A lightweight tool for archiving GitHub repository traffic data (beyond the 14-day limit). It allows users to build long-term analytics by periodically collecting data and visualizing it locally.

## Purpose

GitHub only provides traffic data for the last 14 days. This tool extends that capability by:

- Storing views and clones over time
- Preserving referrers and popular content
- Enabling long-term trend analysis

## How It Works

1. The script connects to the GitHub API using a personal access token.
2. It fetches repository traffic data, including:
   - Views
   - Clones
   - Referrers
   - Popular paths
3. New data is merged with existing data to avoid duplicates.
4. The result is stored in `traffic.json`.
5. The dashboard reads this data and provides visualization.

## Folder Structure

```
github-traffic-archiver/
|──tracker.py     <- Main Script
|──config.json    <- Github Token
|──traffic.json   <- Traffic Data
|──dashboard/
    │──index.html    <- Main Dashboard
    │──app.js        <- Data Logic
    │──style.css     <- UI Style
```

## Setup

1. Install required package:

```bash
pip install requests
```

2. Create a `config.json` file:

```json
{
  "token": "YOUR_GITHUB_TOKEN"
}
```

## Usage

Run the tracker script:

```bash
python tracker.py
```

The script will:
- Fetch latest traffic data
- Merge it with existing data
- Update `traffic.json`

To view the dashboard:
- Open the `dashboard/index.html` file in any browser
- View repository statistics
- Apply date filters using the built-in controls

## Automation (Optional)

To ensure data is not lost, run the script periodically using a cron job:

```bash
0 0 * * * python3 /path/to/tracker.py
```

Running this daily is recommended to maintain a complete history.

## Notes

- GitHub traffic data is limited to 14 days without archiving
- Regular execution is required to preserve data
- No external server is required, the dashboard runs locally

