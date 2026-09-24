"""
CDC Provisional Natality 2025 Dashboard
Entry point: page config, header, sidebar filters, and tab routing.
"""

import streamlit as st

from tabs import (
    about_the_data,
    data_table_download,
    geographic_analysis,
    monthly_sex_analysis,
    overview,
)
from utils.data_loader import DataValidationError, load_data
from utils.filters import render_sidebar_filters


def render_header() -> None:
    st.title("CDC Provisional Natality Dashboard — 2025")
    st.markdown(
        "Explore 2025 U.S. birth counts by **state**, **month**, and **infant sex** "
        "using CDC provisional natality data. Use the filters in the sidebar to "
        "narrow the view; every chart, KPI, and table below responds to your selection."
    )
    st.warning(
        "⚠️ **Provisional data:** figures are preliminary and subject to revision. "
        "**These are birth counts, not birth rates** — they are not adjusted for "
        "population size.",
        icon="⚠️",
    )
    st.caption("Source: CDC National Center for Health Statistics, Provisional Natality data, 2025.")


def main() -> None:
    st.set_page_config(
        page_title="CDC Provisional Natality Dashboard 2025",
        page_icon="👶",
        layout="wide",
    )

    render_header()

    try:
        df = load_data()
    except DataValidationError as e:
        st.error(f"The data file failed validation and cannot be loaded: {e}")
        st.stop()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    filtered_df = render_sidebar_filters(df)

    tab_names = [
        "Overview",
        "Geographic Analysis",
        "Monthly and Sex Analysis",
        "Data Table and Download",
        "About the Data",
    ]
    tab_overview, tab_geo, tab_monthly_sex, tab_table, tab_about = st.tabs(tab_names)

    with tab_overview:
        overview.render(filtered_df)
    with tab_geo:
        geographic_analysis.render(filtered_df)
    with tab_monthly_sex:
        monthly_sex_analysis.render(filtered_df)
    with tab_table:
        data_table_download.render(filtered_df)
    with tab_about:
        about_the_data.render(df)  # unfiltered df: this tab describes the whole dataset


if __name__ == "__main__":
    main()
