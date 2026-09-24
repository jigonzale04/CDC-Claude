import pandas as pd
import streamlit as st


def render(df: pd.DataFrame) -> None:
    st.subheader("About This Data")

    st.markdown(
        """
        **Source:** U.S. Centers for Disease Control and Prevention (CDC), National
        Center for Health Statistics — Provisional Natality data for 2025.

        **⚠️ Provisional data notice:** These figures are *provisional* and subject
        to revision as more complete records are processed. They should not be
        treated as final counts.

        **Birth counts, not birth rates:** Every number in this dashboard is a raw
        count of births. None of the figures are normalized by population, so they
        are **not** birth rates and should not be interpreted as measuring the
        likelihood of birth in a given state — larger states will naturally show
        larger counts.

        **Coverage:** 50 states + the District of Columbia, all 12 months of 2025,
        broken out by reported infant sex (Female / Male).
        """
    )

    if st.session_state.get("data_issues"):
        st.warning("Data validation notes:\n\n" + "\n".join(f"- {i}" for i in st.session_state["data_issues"]))
    else:
        st.success("All data validation checks passed: no missing values, no unexpected categories, "
                    "no duplicate state/month/sex combinations.")

    st.caption(f"Full (unfiltered) dataset: {len(df):,} rows.")
