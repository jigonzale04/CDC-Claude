"""
Sidebar filter widgets: geography, month, and sex multiselects, a
"Select All" convenience per widget, and a "Reset Filters" button that
restores every filter to fully selected via st.session_state.
"""

import pandas as pd
import streamlit as st

STATE_KEY = "filter_states"
MONTH_KEY = "filter_months"
SEX_KEY = "filter_sexes"


def _reset_filters(all_states: list[str], all_months: list[str], all_sexes: list[str]) -> None:
    st.session_state[STATE_KEY] = list(all_states)
    st.session_state[MONTH_KEY] = list(all_months)
    st.session_state[SEX_KEY] = list(all_sexes)


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render all sidebar filter controls and return the filtered
    DataFrame. Also renders a plain-language "active filters" summary."""
    all_states = sorted(df["state_of_residence"].unique().tolist())
    all_months = df["month"].cat.categories.tolist()
    all_sexes = sorted(df["sex_of_infant"].unique().tolist())

    # Initialize session state once, defaulting to "everything selected".
    if STATE_KEY not in st.session_state:
        _reset_filters(all_states, all_months, all_sexes)

    st.sidebar.header("Filters")

    # --- Geography ---
    select_all_states = st.sidebar.checkbox("Select all states/territories", value=True, key="select_all_states")
    if select_all_states:
        st.session_state[STATE_KEY] = list(all_states)
    selected_states = st.sidebar.multiselect(
        "State / geography",
        options=all_states,
        default=st.session_state[STATE_KEY],
        key=STATE_KEY,
    )

    # --- Month ---
    select_all_months = st.sidebar.checkbox("Select all months", value=True, key="select_all_months")
    if select_all_months:
        st.session_state[MONTH_KEY] = list(all_months)
    selected_months = st.sidebar.multiselect(
        "Month",
        options=all_months,
        default=st.session_state[MONTH_KEY],
        key=MONTH_KEY,
    )

    # --- Sex ---
    selected_sexes = st.sidebar.multiselect(
        "Infant sex",
        options=all_sexes,
        default=st.session_state[SEX_KEY],
        key=SEX_KEY,
    )

    st.sidebar.divider()
    if st.sidebar.button("Reset filters", use_container_width=True):
        _reset_filters(all_states, all_months, all_sexes)
        st.rerun()

    # --- Active filter summary ---
    n_states, n_all_states = len(selected_states), len(all_states)
    n_months, n_all_months = len(selected_months), len(all_months)
    n_sexes, n_all_sexes = len(selected_sexes), len(all_sexes)

    states_label = "All states" if n_states == n_all_states else f"{n_states} state(s)"
    months_label = "All months" if n_months == n_all_months else f"{n_months} month(s)"
    sexes_label = "Both sexes" if n_sexes == n_all_sexes else ", ".join(selected_sexes) if selected_sexes else "None selected"

    st.sidebar.caption(f"**Active filters:** {states_label} · {months_label} · {sexes_label}")

    filtered = df[
        df["state_of_residence"].isin(selected_states)
        & df["month"].isin(selected_months)
        & df["sex_of_infant"].isin(selected_sexes)
    ]
    return filtered
