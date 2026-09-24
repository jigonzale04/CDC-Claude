"""KPI summary cards shown at the top of every tab."""

import pandas as pd
import streamlit as st


def render_kpi_cards(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No data matches the current filters. Adjust the filters in the sidebar to see results.")
        return

    total_births = int(df["births"].sum())
    n_geographies = df["state_of_residence"].nunique()

    by_month = df.groupby("month", observed=True)["births"].sum()
    avg_per_month = by_month.mean() if not by_month.empty else 0
    top_month = by_month.idxmax() if not by_month.empty else "N/A"

    by_state = df.groupby("state_of_residence")["births"].sum()
    top_state = by_state.idxmax() if not by_state.empty else "N/A"

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total births (selection)", f"{total_births:,}")
    col2.metric("Geographies selected", f"{n_geographies:,}")
    col3.metric("Avg. births / month", f"{avg_per_month:,.0f}")
    col4.metric("Top geography", str(top_state))
    col5.metric("Top month", str(top_month))
