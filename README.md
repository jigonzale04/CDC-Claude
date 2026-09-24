# CDC Provisional Natality 2025 Dashboard

A Streamlit dashboard for exploring 2025 U.S. provisional birth-count data
by state, month, and infant sex. Built for an undergraduate business
analytics audience.

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app looks for its data file at `data/Provisional_Natality_2025_CDC.csv`,
resolved relative to the project directory — no path changes are needed to
deploy this on Streamlit Community Cloud; just push the whole folder
(including `data/`) to a GitHub repo and point Streamlit Cloud at `app.py`.

## Project structure

```
natality_dashboard/
├── app.py                        # Entry point: page config, header, sidebar, tab router
├── data/
│   └── Provisional_Natality_2025_CDC.csv
├── utils/
│   ├── data_loader.py            # st.cache_data loader + validation checks
│   ├── state_mapping.py          # state name -> USPS abbreviation lookup
│   └── filters.py                # sidebar filter widgets, Select All, Reset
├── components/
│   ├── kpi_cards.py              # the 5 KPI metrics
│   ├── charts.py                 # all 6 Plotly visualizations
│   └── data_table.py             # searchable table + CSV download
├── tabs/
│   ├── overview.py
│   ├── geographic_analysis.py
│   ├── monthly_sex_analysis.py
│   ├── data_table_download.py
│   └── about_the_data.py
└── requirements.txt
```

## Notes on design decisions

- **District of Columbia** is included in every KPI, chart, and table
  except the US state choropleth map, whose underlying map projection
  (Plotly's built-in `USA-states` locations) does not render DC. A note
  appears under the map when DC is part of the active selection.
- **Month ordering** is enforced everywhere via an ordered pandas
  `Categorical` built from the `month_code` column, so charts and
  sorts always read January → December rather than alphabetically.
- **Empty selections**: every chart and the data table detect an empty
  filtered DataFrame and show a friendly message instead of an error or
  a blank plot.
- Figures are **birth counts, not birth rates** — this is stated in the
  header and in the About the Data tab, and no per-capita normalization
  is applied anywhere in the app.
