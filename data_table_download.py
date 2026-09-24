import pandas as pd

from components.data_table import render_data_table
from components.kpi_cards import render_kpi_cards


def render(df: pd.DataFrame) -> None:
    render_kpi_cards(df)
    render_data_table(df)
