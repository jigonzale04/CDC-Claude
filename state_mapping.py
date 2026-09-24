"""
Reliable state-name -> USPS abbreviation mapping.

Used for the choropleth map, which needs 2-letter USPS codes
(plotly's built-in USA-states locationmode). District of Columbia
is not part of the standard 50-state locationmode set supported by
plotly's built-in USA geometries, so it is deliberately excluded
from the choropleth (a note is shown to the user) but is retained
everywhere else (rankings, KPIs, tables, heatmap, trend lines).
"""

STATE_TO_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
    # Not plotted on the choropleth (see module docstring) but kept for
    # completeness elsewhere in the app.
    "District of Columbia": "DC",
}

# States excluded specifically from map rendering (choropleth), not from
# any other analysis in the dashboard.
MAP_UNSUPPORTED_STATES = {"District of Columbia"}


def get_abbr(state_name: str) -> str:
    """Return the USPS abbreviation for a state name, or the original
    string if it is not recognized (fails loudly rather than silently
    dropping data elsewhere in the app)."""
    return STATE_TO_ABBR.get(state_name, state_name)
