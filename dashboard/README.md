# Esports Earnings Dashboard

An interactive Plotly Dash dashboard built on the data from `esports_dataset_export.csv`.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:8050** in your browser.

## Features

- **Filters**: multi-select dropdowns for Genre, Continent, and Game, plus a one-click reset button. All charts and KPIs update together.
- **KPI cards**: total prize money, player count, game count, country count, average prize per player recalculated live from the current filter selection.
- **Genre bar chart**: total prize money by genre.
- **Continent donut chart**: share of prize money by continent.
- **Treemap**: prize money by individual game, grouped by genre (click to zoom in/out).
- **Top 15 players bar chart**: highest-earning individual players, with game shown on hover.
- **Release year scatter**: prize money vs. the game's release year, bubble size = prize money, colored by genre.
- **Sortable/filterable data table**: every player row, with a built-in search box per column.
