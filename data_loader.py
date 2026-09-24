"""
Data loading and validation for the natality dashboard.

Loading is cached with st.cache_data so the CSV is parsed once per
session (until the underlying file changes), keeping the app responsive
as filters are toggled.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

EXPECTED_COLUMNS = {
    "state_of_residence",
    "month",
    "month_code",
    "year_code",
    "sex_of_infant",
    "births",
}

EXPECTED_SEXES = {"Female", "Male"}
EXPECTED_MONTH_CODES = set(range(1, 13))

# Data file lives alongside the package, so this path resolves correctly
# whether the app is run locally (`streamlit run app.py`) or deployed on
# Streamlit Community Cloud, regardless of the working directory the
# process was launched from.
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Provisional_Natality_2025_CDC.csv"


class DataValidationError(Exception):
    """Raised when the source CSV fails a basic sanity check."""


def _validate(df: pd.DataFrame) -> list[str]:
    """Run a set of basic data-quality checks and return a list of
    human-readable warning/error strings (empty list = all clear)."""
    issues = []

    missing_cols = EXPECTED_COLUMNS - set(df.columns)
    if missing_cols:
        issues.append(f"Missing expected column(s): {sorted(missing_cols)}")
        # Can't safely check anything else without the columns present.
        return issues

    if df["births"].isnull().any():
        issues.append("Some 'births' values are missing (null).")

    if (df["births"] < 0).any():
        issues.append("Some 'births' values are negative, which is not physically valid.")

    bad_sexes = set(df["sex_of_infant"].unique()) - EXPECTED_SEXES
    if bad_sexes:
        issues.append(f"Unexpected value(s) in 'sex_of_infant': {sorted(bad_sexes)}")

    bad_months = set(df["month_code"].unique()) - EXPECTED_MONTH_CODES
    if bad_months:
        issues.append(f"Unexpected value(s) in 'month_code': {sorted(bad_months)}")

    if df.duplicated(subset=["state_of_residence", "month_code", "sex_of_infant"]).any():
        issues.append("Duplicate (state, month, sex) combinations found.")

    return issues


@st.cache_data(show_spinner="Loading natality data...")
def load_data() -> pd.DataFrame:
    """Load, validate, and lightly enrich the natality dataset.

    Returns a DataFrame with an added categorical `month` column that
    preserves chronological order (Jan -> Dec) for correct sorting in
    charts and widgets, regardless of alphabetical ordering.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Could not find the data file at {DATA_PATH}. "
            "Make sure the CSV ships alongside the app under data/."
        )

    df = pd.read_csv(DATA_PATH)

    issues = _validate(df)
    if issues:
        # Surface issues to the user rather than failing silently, but
        # don't crash the whole app over data-quality warnings unless the
        # required columns themselves are missing.
        st.session_state["data_issues"] = issues
        if "Missing expected column(s)" in issues[0]:
            raise DataValidationError("; ".join(issues))
    else:
        st.session_state["data_issues"] = []

    # Ordered categorical so every groupby/sort respects Jan -> Dec order.
    month_order = (
        df[["month", "month_code"]]
        .drop_duplicates()
        .sort_values("month_code")["month"]
        .tolist()
    )
    df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)

    return df
