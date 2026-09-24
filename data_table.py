"""Searchable filtered data table with a CSV download button."""

import pandas as pd
import streamlit as st


def render_data_table(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No data matches the current filters. Adjust the filters in the sidebar to see results.")
        return

    search_term = st.text_input(
        "Search table (matches any state name)",
        placeholder="e.g. Texas",
    )

    display_df = df.copy()
    display_df["month"] = display_df["month"].astype(str)  # drop categorical dtype for display/export

    if search_term:
        display_df = display_df[
            display_df["state_of_residence"].str.contains(search_term, case=False, na=False)
        ]

    st.dataframe(
        display_df.rename(
            columns={
                "state_of_residence": "State",
                "month": "Month",
                "month_code": "Month #",
                "year_code": "Year",
                "sex_of_infant": "Sex",
                "births": "Births",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(f"Showing {len(display_df):,} of {len(df):,} filtered rows.")

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv_bytes,
        file_name="natality_filtered_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
