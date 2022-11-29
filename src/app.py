import streamlit as st
import st_aggrid
import pandas as pd

import core
from core import validate
import models

st.set_page_config(layout="wide")

# initialize state
state_keys = {
    "selected_rows": pd.DataFrame(),
    # "rows_with_warnings": pd.DataFrame(),
    # "failed_br_rows": pd.DataFrame(),
}

for key, val in state_keys.items():
    if key not in st.session_state:
        st.session_state[key] = val

if "data" not in st.session_state:
    data_loader = st.cache(allow_output_mutation=True)(core.load_data)
    df = data_loader()
    st.session_state["data"] = df
else:
    df = st.session_state["data"]

if "rows_with_warnings" not in st.session_state:
    rows = validate.apply_warnings(df)
    # print("WARNINGS", rows)
    rows_with_warnings = pd.DataFrame(rows)
    if not rows_with_warnings.empty:
        rows_with_warnings.set_index("id", drop=False)
    st.session_state["rows_with_warnings"] = rows_with_warnings
else:
    rows_with_warnings = st.session_state["rows_with_warnings"]

if not rows_with_warnings.empty:
    count = rows_with_warnings.drop(columns=["id"]).sum(axis=1)
    # print("WARNINGS", count)
else:
    df["Warnings"] = 0
    st.session_state["data"] =df

if "failed_br_rows" not in st.session_state:
    rows = validate.apply_business_rules(df)
    # print("FAILED", rows)
    failed_rows = pd.DataFrame(rows).set_index("id", drop=False)
    st.session_state["failed_br_rows"] = failed_rows
else:
    failed_rows = st.session_state["failed_br_rows"]

if not failed_rows.empty:
    count = failed_rows.drop(columns=["id"]).sum(axis=1)
    df["Failed_Business_Rules"] = count
else:
    df["Failed_Business_Rules"] = 0
    st.session_state["data"] = df




#Infer basic colDefs from dataframe types
gb = st_aggrid.GridOptionsBuilder.from_dataframe(df)

# configure row selection
gb.configure_selection(
    selection_mode="multiple",
    use_checkbox=True
)

# configure pagination
gb.configure_pagination(
    enabled=True,
    paginationPageSize=True
)

# configure column options
gb.configure_default_column(
    editable=True
)

grid_response: models.GridResponse = st_aggrid.AgGrid(
    data=df,
    height=500,
    gridOptions=gb.build(),
    width='100%',
    columns_auto_size_mode=st_aggrid.ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
    update_on=[("cellValueChanged", 100)],
    data_return_mode=st_aggrid.DataReturnMode.FILTERED_AND_SORTED,  # no idea what this does
)


df = grid_response['data']
selected = grid_response['selected_rows']
# print(type(selected))
# print(selected)
selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')
# print("selection", selected_df)
# print("full data", grid_response['data'])
# print(dir(grid_response))
# print(grid_response.column_state)
# print(df.head(10))

# add_load = st.sidebar.button("Load CSV", on_click=data_loader)