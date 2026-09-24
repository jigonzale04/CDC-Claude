import pandas as pd
import streamlit as st

from components import charts
from components.kpi_cards import render_kpi_cards


def render(df: pd.DataFrame) -> None:
    render_kpi_cards(df)
    st.divider()

    st.plotly_chart(charts.sex_comparison_chart(df), use_container_width=True)
    st.plotly_chart(charts.monthly_trend_chart(df), use_container_width=True)
    st.plotly_chart(charts.state_month_heatmap(df), use_container_width=True)
