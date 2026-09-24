"""
All visualizations for the dashboard, built with Plotly.

Design choices applied consistently across every chart:
- A colorblind-safe, categorical palette (Plotly's "Safe" sequence) for
  any chart that encodes a categorical variable (e.g., sex).
- A continuous, perceptually uniform scale (Viridis) for the choropleth
  and heatmap, which encode a numeric quantity.
- No truncated/non-zero-based axes on bar or line charts, so bar length
  and line height are never visually misleading.
- Thousands separators on hover text and axis ticks.
- Every chart has a descriptive title and axis labels.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.state_mapping import MAP_UNSUPPORTED_STATES, get_abbr

CATEGORICAL_PALETTE = px.colors.qualitative.Safe
SEQUENTIAL_SCALE = "Viridis"


def _empty_figure_message(message: str) -> go.Figure:
    """A blank figure carrying only a centered message, used whenever a
    filter selection leaves nothing to plot."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        showarrow=False,
        font={"size": 16},
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def monthly_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Line chart: total births by month, chronologically ordered."""
    if df.empty:
        return _empty_figure_message("No data for the current filter selection.")

    monthly = df.groupby("month", observed=True)["births"].sum().reset_index()
    monthly = monthly.sort_values("month")

    fig = px.line(
        monthly,
        x="month",
        y="births",
        markers=True,
        title="Monthly Birth Trend (Selected Geographies & Sexes)",
        labels={"month": "Month", "births": "Total Births"},
        color_discrete_sequence=CATEGORICAL_PALETTE,
    )
    fig.update_traces(hovertemplate="%{x}<br>Births: %{y:,}<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",")
    return fig


def sex_comparison_chart(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart: female vs. male births by month."""
    if df.empty:
        return _empty_figure_message("No data for the current filter selection.")

    by_sex_month = (
        df.groupby(["month", "sex_of_infant"], observed=True)["births"].sum().reset_index()
    )
    by_sex_month = by_sex_month.sort_values("month")

    fig = px.bar(
        by_sex_month,
        x="month",
        y="births",
        color="sex_of_infant",
        barmode="group",
        title="Female vs. Male Births by Month",
        labels={"month": "Month", "births": "Total Births", "sex_of_infant": "Sex"},
        color_discrete_sequence=CATEGORICAL_PALETTE,
    )
    fig.update_traces(hovertemplate="%{x}<br>Births: %{y:,}<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",")
    return fig


def state_ranking_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Horizontal bar chart ranking geographies by total births."""
    if df.empty:
        return _empty_figure_message("No data for the current filter selection.")

    by_state = df.groupby("state_of_residence")["births"].sum().sort_values(ascending=False)
    by_state = by_state.head(top_n).sort_values()  # ascending for horizontal bar readability

    fig = px.bar(
        by_state,
        x=by_state.values,
        y=by_state.index,
        orientation="h",
        title=f"Top {min(top_n, len(by_state))} Geographies by Total Births",
        labels={"x": "Total Births", "y": "Geography"},
        color_discrete_sequence=CATEGORICAL_PALETTE,
    )
    fig.update_traces(hovertemplate="%{y}<br>Births: %{x:,}<extra></extra>")
    fig.update_xaxes(rangemode="tozero", tickformat=",")
    return fig


def choropleth_map(df: pd.DataFrame) -> go.Figure:
    """US state choropleth of total births in the current selection.

    District of Columbia is excluded from this map (plotly's built-in
    USA-states geometries don't render it) but remains included in
    every other chart, KPI, and table in the dashboard.
    """
    if df.empty:
        return _empty_figure_message("No data for the current filter selection.")

    mappable = df[~df["state_of_residence"].isin(MAP_UNSUPPORTED_STATES)]
    if mappable.empty:
        return _empty_figure_message("Selection only includes geographies not supported by the map view.")

    by_state = mappable.groupby("state_of_residence")["births"].sum().reset_index()
    by_state["abbr"] = by_state["state_of_residence"].map(get_abbr)

    fig = px.choropleth(
        by_state,
        locations="abbr",
        locationmode="USA-states",
        color="births",
        scope="usa",
        color_continuous_scale=SEQUENTIAL_SCALE,
        title="Total Births by State (Selected Filters)",
        labels={"births": "Total Births"},
        hover_name="state_of_residence",
    )
    fig.update_traces(hovertemplate="%{hovertext}<br>Births: %{z:,}<extra></extra>")

    excluded = mappable is not df
    if set(df["state_of_residence"]) & MAP_UNSUPPORTED_STATES:
        fig.add_annotation(
            text="Note: District of Columbia is not shown on this map (unsupported by the map projection) "
                 "but is included in all other charts and totals.",
            showarrow=False,
            xref="paper", yref="paper", x=0.5, y=-0.12,
            font={"size": 11},
        )
    return fig


def state_month_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap of total births, months on the Y-axis (12 rows) and
    states on the X-axis, chosen over the transpose for readability
    since months are far fewer than states."""
    if df.empty:
        return _empty_figure_message("No data for the current filter selection.")

    pivot = (
        df.groupby(["month", "state_of_residence"], observed=True)["births"]
        .sum()
        .reset_index()
        .pivot(index="month", columns="state_of_residence", values="births")
    )
    pivot = pivot.reindex(df["month"].cat.categories)  # keep chronological order

    fig = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale=SEQUENTIAL_SCALE,
        title="Births by State and Month",
        labels={"x": "State", "y": "Month", "color": "Births"},
    )
    fig.update_traces(hovertemplate="State: %{x}<br>Month: %{y}<br>Births: %{z:,}<extra></extra>")
    fig.update_xaxes(tickangle=-60)
    return fig


def top_bottom_comparison_chart(df: pd.DataFrame, n: int = 5) -> go.Figure:
    """Side-by-side comparison of the top-N and bottom-N geographies by
    total births within the current selection."""
    if df.empty:
        return _empty_figure_message("No data for the current filter selection.")

    by_state = df.groupby("state_of_residence")["births"].sum().sort_values(ascending=False)
    n = min(n, len(by_state) // 2) if len(by_state) >= 2 else len(by_state)
    if n == 0:
        return _empty_figure_message("Not enough geographies selected for a top/bottom comparison.")

    top = by_state.head(n).reset_index()
    top["group"] = f"Top {n}"
    bottom = by_state.tail(n).reset_index()
    bottom["group"] = f"Bottom {n}"
    combined = pd.concat([top, bottom], ignore_index=True)

    fig = px.bar(
        combined,
        x="births",
        y="state_of_residence",
        color="group",
        orientation="h",
        title=f"Top {n} vs. Bottom {n} Geographies by Total Births",
        labels={"births": "Total Births", "state_of_residence": "Geography", "group": ""},
        color_discrete_sequence=CATEGORICAL_PALETTE,
    )
    fig.update_traces(hovertemplate="%{y}<br>Births: %{x:,}<extra></extra>")
    fig.update_xaxes(rangemode="tozero", tickformat=",")
    fig.update_layout(barmode="group")
    return fig
