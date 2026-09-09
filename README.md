# 🎮 Esports Earnings Analytics & Dashboard

[![Python](https://shields.io)](https://python.org)
[![Dash](https://shields.io)](https://plotly.com)
[![Pandas](https://shields.io)](https://pydata.org)

Welcome to the **Esports Earnings Analytics and Dashboard** project! This repository showcases an end-to-end data analytics workflow within the highly competitive and rapidly growing esports industry. From ingesting and cleaning raw datasets to developing an interactive web application, this project extracts valuable and actionable business insights.

Which gaming genres dominate the financial landscape? How does the size of a player base impact overall prize pools? Is Europe outearning Asia? This project answers these questions through data-driven storytelling.

---

## 📈 Executive Summary and Key Insights

The initial exploratory data analysis (EDA), conducted inside the project's notebooks (`.ipynb` files), revealed distinct and fascinating industry dynamics:
* **The Pareto Principle of Esports Data:** A tiny elite of top-tier games captures the vast majority of all-time global prize pools.
* **The MOBA Empire:** Multiplayer Online Battle Arena games (such as *Dota 2* and *League of Legends*) completely eclipse other categories when it comes to cash prizes.
* **Player Base vs. Cash Prizes (r = 0.72):** Statistical testing confirms a very strong positive correlation between a game's competitive player count and its total financial return. Larger active communities drive publisher investment.

---

## 💻 The Interactive Dashboard

To turn these insights into an operational tool, the data pipeline feeds a **fully interactive web application** built with **Dash (Plotly)**.

### Key Features:
* **Dynamic Cross-Filtering:** Seamless multi-select dropdowns for *Genre*, *Continent*, and *Game* with a one-click global reset button. Every chart and metric updates in real-time based on your selection.
* **Live KPI Cards:** Instant calculation of Total Prize Pools, active pro player counts, total games tracked, unique countries involved, and average prize earnings per player.
* **Advanced Visualizations:**
  * An interactive **Treemap** grouping individual games inside their parent genres (supports click-to-zoom).
  * A **Donut Chart** breaking down market share by continent.
  * A **Bubble Scatter Plot** mapping prize pools against a game's historical release year, categorized by genre.
* **Auditable Data Table:** A comprehensive backend table featuring built-in column sorting and dedicated text filters per column to drill down to specific player profiles.

---

## 📁 Repository Structure

The project directory is structured using industry best practices, separating the R&D/exploration phase from the final production application:

```text
├── dashboard/                     # Production Dashboard Folder
│   ├── app.py                     # Main Dash web application (Layout and Callbacks)
│   ├── requirements.txt           # Deployment dependencies
│   └── README.md                  # Technical installation guide for the app
├── earnings_by_games_and_genre.ipynb # Advanced EDA Notebook (Seaborn/Matplotlib viz)
├── Esport_test.ipynb              # Ingestion, validation, and data cleaning Notebook
├── esports_dataset_export.csv      # Complete player-level master dataset
└── game_data_by_genre.csv          # Aggregated game-level dataset
```

---

## 🚀 Getting Started

The code for the interactive dashboard and its internal environment configurations are fully contained within the `dashboard/` directory. 

To set up the environment, install the dependencies, and launch the dashboard application locally on your machine, please follow the step-by-step instructions provided in the dedicated guide:

👉 **[Dashboard Installation and Deployment Guide](./dashboard/README.md)**

---

## 🛠️ Technical Stack

* **Language:** Python 3.12
* **Data Manipulation and Ingestion:** Pandas, NumPy
* **Exploratory Data Analysis and Viz:** Matplotlib, Seaborn
* **Web Framework and Interactive Charts:** Dash, Plotly Express

---

*If you find this project resourceful or interesting, feel free to leave a star 🌟 on the repository or open an Issue for feature suggestions!*
