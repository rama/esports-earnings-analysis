import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from dash.dash_table import DataTable

players = pd.read_csv("../esports_dataset_export.csv")

players["PlayerName"] = players["NameFirst"].str.strip() + " " + players["NameLast"].str.strip()

GENRES = sorted(players["Genre"].dropna().unique())
CONTINENTS = sorted(players["Continent_Name"].dropna().unique())
GAMES = sorted(players["Game"].dropna().unique())

COLOR_MAP = px.colors.qualitative.Set2
TEMPLATE = "plotly_white"

app = Dash(__name__, title="Esports Earnings Dashboard")
server = app.server

CARD_STYLE = {
    "background": "#ffffff",
    "borderRadius": "12px",
    "padding": "18px 22px",
    "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
    "flex": "1",
    "minWidth": "180px",
}

GRAPH_CARD_STYLE = {
    "background": "#ffffff",
    "borderRadius": "12px",
    "padding": "12px",
    "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
    "marginBottom": "20px",
}

VISIBLE_STYLES = {
    "genre-bar-wrap": {**GRAPH_CARD_STYLE, "flex": "1.3", "minWidth": "420px"},
    "game-bar-wrap": {**GRAPH_CARD_STYLE, "flex": "1.3", "minWidth": "420px"},
    "continent-pie-wrap": {**GRAPH_CARD_STYLE, "flex": "1", "minWidth": "320px"},
    "game-treemap-wrap": {**GRAPH_CARD_STYLE},
    "country-bar-wrap": {**GRAPH_CARD_STYLE},
    "top-players-wrap": {**GRAPH_CARD_STYLE, "flex": "1", "minWidth": "420px"},
    "release-year-wrap": {**GRAPH_CARD_STYLE, "flex": "1", "minWidth": "420px"},
}
HIDDEN_STYLE = {"display": "none"}


def kpi_card(label, value_id):
    return html.Div(
        [
            html.Div(label, style={"fontSize": "13px", "color": "#6b7280", "fontWeight": "600",
                                    "textTransform": "uppercase", "letterSpacing": "0.03em"}),
            html.Div(id=value_id, style={"fontSize": "28px", "fontWeight": "700", "color": "#111827",
                                          "marginTop": "6px"}),
        ],
        style=CARD_STYLE,
    )


app.layout = html.Div(
    style={"backgroundColor": "#f3f4f6", "minHeight": "100vh", "fontFamily": "Inter, Helvetica, Arial, sans-serif",
           "padding": "24px 32px"},
    children=[
        html.Div(
            [
                html.H1("🎮 Esports Earnings Dashboard", style={"margin": "0", "fontSize": "30px",
                                                                  "color": "#111827"}),
                html.P("Explore prize money earned by professional esports players across games, genres, "
                       "and regions. Pick a genre, then a game, to drill down.",
                       style={"color": "#6b7280", "marginTop": "6px"}),
            ],
            style={"marginBottom": "24px"},
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Label("Genre", style={"fontWeight": "600", "fontSize": "13px", "color": "#374151"}),
                        dcc.Dropdown(
                            id="genre-filter",
                            options=[{"label": g, "value": g} for g in GENRES],
                            value=[],
                            multi=True,
                            placeholder="All genres",
                        ),
                    ],
                    style={"flex": "1", "minWidth": "220px"},
                ),
                html.Div(
                    [
                        html.Label("Continent", style={"fontWeight": "600", "fontSize": "13px", "color": "#374151"}),
                        dcc.Dropdown(
                            id="continent-filter",
                            options=[{"label": c, "value": c} for c in CONTINENTS],
                            value=[],
                            multi=True,
                            placeholder="All continents",
                        ),
                    ],
                    style={"flex": "1", "minWidth": "220px"},
                ),
                html.Div(
                    [
                        html.Label("Game", style={"fontWeight": "600", "fontSize": "13px", "color": "#374151"}),
                        dcc.Dropdown(
                            id="game-filter",
                            options=[{"label": g, "value": g} for g in GAMES],
                            value=[],
                            multi=True,
                            placeholder="All games",
                        ),
                    ],
                    style={"flex": "1", "minWidth": "220px"},
                ),
                html.Div(
                    html.Button("Reset filters", id="reset-btn", n_clicks=0, style={
                        "padding": "10px 16px", "borderRadius": "8px", "border": "1px solid #d1d5db",
                        "background": "#ffffff", "cursor": "pointer", "fontWeight": "600", "color": "#374151",
                        "marginTop": "20px",
                    }),
                    style={"display": "flex", "alignItems": "flex-end"},
                ),
            ],
            style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px",
                   **CARD_STYLE, "alignItems": "flex-end"},
        ),

        # KPI row
        html.Div(
            [
                kpi_card("Total Prize Money", "kpi-total-prize"),
                kpi_card("Players", "kpi-players"),
                kpi_card("Games", "kpi-games"),
                kpi_card("Countries", "kpi-countries"),
                kpi_card("Avg. Prize / Player", "kpi-avg-prize"),
            ],
            style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"},
        ),

        # Row 1
        html.Div(
            [
                html.Div(dcc.Graph(id="genre-bar", config={"displayModeBar": False}), id="genre-bar-wrap"),
                html.Div(dcc.Graph(id="game-bar", config={"displayModeBar": False}), id="game-bar-wrap"),
                html.Div(dcc.Graph(id="continent-pie", config={"displayModeBar": False}), id="continent-pie-wrap"),
            ],
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
        ),

        # Row 2
        html.Div(
            [
                html.Div(dcc.Graph(id="game-treemap", config={"displayModeBar": False}), id="game-treemap-wrap"),
                html.Div(dcc.Graph(id="country-bar", config={"displayModeBar": False}), id="country-bar-wrap"),
            ],
        ),

        # Row 3
        html.Div(
            [
                html.Div(dcc.Graph(id="top-players-bar", config={"displayModeBar": False}), id="top-players-wrap"),
                html.Div(dcc.Graph(id="release-year-scatter", config={"displayModeBar": False}),
                         id="release-year-wrap"),
            ],
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
        ),

        # Row 4
        html.Div(
            [
                html.H3("Player Detail", style={"marginTop": "0"}),
                DataTable(
                    id="player-table",
                    columns=[
                        {"name": "Player", "id": "PlayerName"},
                        {"name": "Handle", "id": "CurrentHandle"},
                        {"name": "Game", "id": "Game"},
                        {"name": "Genre", "id": "Genre"},
                        {"name": "Country", "id": "Country_Name"},
                        {"name": "Total Prize (USD)", "id": "TotalUSDPrize", "type": "numeric",
                         "format": {"specifier": ",.2f"}},
                    ],
                    page_size=12,
                    sort_action="native",
                    filter_action="native",
                    style_table={"overflowX": "auto"},
                    style_cell={"padding": "8px", "fontFamily": "Inter, Helvetica, Arial, sans-serif",
                                "fontSize": "13px"},
                    style_header={"backgroundColor": "#f9fafb", "fontWeight": "700", "color": "#374151"},
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "#fafafa"}
                    ],
                ),
            ],
            style=GRAPH_CARD_STYLE,
        ),

        html.Div(
            "Data source: Esports Earnings",
            style={"textAlign": "center", "color": "#9ca3af", "fontSize": "12px", "marginTop": "10px"},
        ),
    ],
)

@app.callback(
    Output("genre-filter", "options"),
    Output("game-filter", "options"),
    Input("genre-filter", "value"),
    Input("continent-filter", "value"),
    Input("game-filter", "value"),
)
def update_dropdown_options(genres, continents, games):
    dff_for_games = players.copy()
    if genres:
        dff_for_games = dff_for_games[dff_for_games["Genre"].isin(genres)]
    if continents:
        dff_for_games = dff_for_games[dff_for_games["Continent_Name"].isin(continents)]
    game_options = [{"label": g, "value": g} for g in sorted(dff_for_games["Game"].dropna().unique())]

    dff_for_genres = players.copy()
    if games:
        dff_for_genres = dff_for_genres[dff_for_genres["Game"].isin(games)]
    if continents:
        dff_for_genres = dff_for_genres[dff_for_genres["Continent_Name"].isin(continents)]
    genre_options = [{"label": g, "value": g} for g in sorted(dff_for_genres["Genre"].dropna().unique())]

    return genre_options, game_options


@app.callback(
    Output("genre-filter", "value"),
    Output("continent-filter", "value"),
    Output("game-filter", "value"),
    Input("reset-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks):
    return [], [], []


def filter_data(genres, continents, games):
    dff = players.copy()
    if genres:
        dff = dff[dff["Genre"].isin(genres)]
    if continents:
        dff = dff[dff["Continent_Name"].isin(continents)]
    if games:
        dff = dff[dff["Game"].isin(games)]
    return dff


def get_state(genres, games):
    if games:
        return "game"
    if genres:
        return "genre"
    return "overview"


@app.callback(
    Output("kpi-total-prize", "children"),
    Output("kpi-players", "children"),
    Output("kpi-games", "children"),
    Output("kpi-countries", "children"),
    Output("kpi-avg-prize", "children"),
    Output("genre-bar", "figure"),
    Output("genre-bar-wrap", "style"),
    Output("game-bar", "figure"),
    Output("game-bar-wrap", "style"),
    Output("continent-pie", "figure"),
    Output("continent-pie-wrap", "style"),
    Output("game-treemap", "figure"),
    Output("game-treemap-wrap", "style"),
    Output("country-bar", "figure"),
    Output("country-bar-wrap", "style"),
    Output("top-players-bar", "figure"),
    Output("top-players-wrap", "style"),
    Output("release-year-scatter", "figure"),
    Output("release-year-wrap", "style"),
    Output("player-table", "data"),
    Input("genre-filter", "value"),
    Input("continent-filter", "value"),
    Input("game-filter", "value"),
)
def update_dashboard(genres, continents, games):
    dff = filter_data(genres, continents, games)
    state = get_state(genres, games)

    total_prize = dff["TotalUSDPrize"].sum()
    n_players = len(dff)
    n_games = dff["Game"].nunique()
    n_countries = dff["Country_Name"].nunique()
    avg_prize = dff["TotalUSDPrize"].mean() if n_players else 0

    kpi_total = f"${total_prize:,.0f}"
    kpi_players = f"{n_players:,}"
    kpi_games = f"{n_games:,}"
    kpi_countries = f"{n_countries:,}"
    kpi_avg = f"${avg_prize:,.0f}"

    fig_genre = px.bar(title="Total Prize Money by Genre")
    if state == "overview":
        genre_totals = (
            players.groupby("Genre", as_index=False)["TotalUSDPrize"].sum()
            .sort_values("TotalUSDPrize", ascending=True)
        )
        if continents:
            genre_totals = (
                dff.groupby("Genre", as_index=False)["TotalUSDPrize"].sum().sort_values("TotalUSDPrize")
            )
        fig_genre = px.bar(
            genre_totals, x="TotalUSDPrize", y="Genre", orientation="h",
            title="Total Prize Money by Genre", template=TEMPLATE, color="Genre",
            color_discrete_sequence=COLOR_MAP,
        )
        fig_genre.update_layout(showlegend=False, xaxis_title="Total prize (USD)", yaxis_title="",
                                 margin=dict(l=10, r=10, t=50, b=10))
        fig_genre.update_traces(hovertemplate="%{y}: $%{x:,.0f}<extra></extra>")

    fig_game_bar = px.bar(title="Total Prize Money by Game")
    if state == "genre":
        game_totals = (
            dff.groupby("Game", as_index=False)["TotalUSDPrize"].sum().sort_values("TotalUSDPrize", ascending=True)
        )
        fig_game_bar = px.bar(
            game_totals, x="TotalUSDPrize", y="Game", orientation="h",
            title=f"Total Prize Money by Game — {', '.join(genres)}", template=TEMPLATE, color="Game",
            color_discrete_sequence=COLOR_MAP,
        )
        fig_game_bar.update_layout(showlegend=False, xaxis_title="Total prize (USD)", yaxis_title="",
                                    margin=dict(l=10, r=10, t=50, b=10))
        fig_game_bar.update_traces(hovertemplate="%{y}: $%{x:,.0f}<extra></extra>")

    cont_totals = dff.groupby("Continent_Name", as_index=False)["TotalUSDPrize"].sum()
    fig_continent = px.pie(
        cont_totals, names="Continent_Name", values="TotalUSDPrize",
        title="Prize Share by Continent", template=TEMPLATE, hole=0.45,
        color_discrete_sequence=COLOR_MAP,
    )
    fig_continent.update_traces(textinfo="percent+label", hovertemplate="%{label}: $%{value:,.0f}<extra></extra>")
    fig_continent.update_layout(margin=dict(l=10, r=10, t=50, b=10))

    fig_treemap = px.treemap(title="Prize Money by Game")
    if state == "overview":
        game_totals_tm = dff.groupby(["Genre", "Game"], as_index=False)["TotalUSDPrize"].sum()
        game_totals_tm = game_totals_tm[game_totals_tm["TotalUSDPrize"] > 0]
        path = ["Genre", "Game"]
        title = "Prize Money by Game (grouped by Genre)"
    
        if len(game_totals_tm):
            fig_treemap = px.treemap(
                game_totals_tm, path=path, values="TotalUSDPrize",
                title=title, template=TEMPLATE,
                color="Genre" if state == "overview" else "Game", color_discrete_sequence=COLOR_MAP,
            )
            fig_treemap.update_traces(hovertemplate="%{label}<br>$%{value:,.0f}<extra></extra>")
        else:
            fig_treemap = px.treemap(title=f"{title} — no data for this filter")
        fig_treemap.update_layout(margin=dict(l=10, r=10, t=50, b=10))

    fig_country = px.bar(title="Prize Money by Country")
    if state == "game":
        country_totals = (
            dff.groupby("Country_Name", as_index=False)["TotalUSDPrize"].sum()
            .sort_values("TotalUSDPrize", ascending=False).head(20)
            .sort_values("TotalUSDPrize", ascending=True)
        )
        fig_country = px.bar(
            country_totals, x="TotalUSDPrize", y="Country_Name", orientation="h",
            title=f"Prize Money by Country — {', '.join(games)}", template=TEMPLATE,
            color_discrete_sequence=["#2563eb"],
        )
        fig_country.update_layout(xaxis_title="Total prize (USD)", yaxis_title="",
                                   margin=dict(l=10, r=10, t=50, b=10))
        fig_country.update_traces(hovertemplate="%{y}: $%{x:,.0f}<extra></extra>")

    if state == "game":
        top_players = dff.sort_values("TotalUSDPrize", ascending=False).head(40).sort_values("TotalUSDPrize")
        title = f"Players by Total Prize Money — {', '.join(games)}"
    else:
        top_players = dff.sort_values("TotalUSDPrize", ascending=False).head(15).sort_values("TotalUSDPrize")
        title = "Top 15 Players by Total Prize Money"

    fig_top = px.bar(
        top_players, x="TotalUSDPrize", y="CurrentHandle", orientation="h",
        title=title, template=TEMPLATE,
        hover_data={"PlayerName": True, "Game": True},
        color_discrete_sequence=["#2563eb"],
    )
    fig_top.update_layout(xaxis_title="Total prize (USD)", yaxis_title="", margin=dict(l=10, r=10, t=50, b=10))
    fig_top.update_traces(hovertemplate="%{y}<br>%{customdata[0]} — %{customdata[1]}<br>$%{x:,.0f}<extra></extra>")

    fig_year = px.scatter(title="Prize Money vs. Game Release Year")
    if state in ("overview", "genre"):
        year_totals = (
            dff.dropna(subset=["ReleaseYear"])
            .groupby(["Game", "ReleaseYear", "Genre"], as_index=False)["TotalUSDPrize"].sum()
        )
        if len(year_totals):
            fig_year = px.scatter(
                year_totals, x="ReleaseYear", y="TotalUSDPrize", size="TotalUSDPrize", color="Genre",
                hover_name="Game", template=TEMPLATE, title="Prize Money vs. Game Release Year",
                color_discrete_sequence=COLOR_MAP, size_max=40,
            )
            fig_year.update_layout(xaxis_title="Release year", yaxis_title="Total prize (USD)",
                                    margin=dict(l=10, r=10, t=50, b=10))
            fig_year.update_traces(hovertemplate="%{hovertext}<br>Year: %{x}<br>$%{y:,.0f}<extra></extra>")
        else:
            fig_year = px.scatter(title="Prize Money vs. Game Release Year — no data for this filter")

    table_data = dff.sort_values("TotalUSDPrize", ascending=False)[
        ["PlayerName", "CurrentHandle", "Game", "Genre", "Country_Name", "TotalUSDPrize"]
    ].to_dict("records")

    genre_bar_style = VISIBLE_STYLES["genre-bar-wrap"] if state == "overview" else HIDDEN_STYLE
    game_bar_style = VISIBLE_STYLES["game-bar-wrap"] if state == "genre" else HIDDEN_STYLE
    treemap_style = VISIBLE_STYLES["game-treemap-wrap"] if state == "overview" else HIDDEN_STYLE
    country_bar_style = VISIBLE_STYLES["country-bar-wrap"] if state == "game" else HIDDEN_STYLE
    release_year_style = VISIBLE_STYLES["release-year-wrap"] if state in ("overview", "genre") else HIDDEN_STYLE
    fig_continent_style = VISIBLE_STYLES["continent-pie-wrap"]
    fig_top_style = VISIBLE_STYLES["top-players-wrap"]

    return (
        kpi_total, kpi_players, kpi_games, kpi_countries, kpi_avg,
        fig_genre, genre_bar_style,
        fig_game_bar, game_bar_style,
        fig_continent, fig_continent_style,
        fig_treemap, treemap_style,
        fig_country, country_bar_style,
        fig_top, fig_top_style,
        fig_year, release_year_style,
        table_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
