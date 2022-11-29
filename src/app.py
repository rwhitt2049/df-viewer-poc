import streamlit as st
import st_aggrid
import pandas as pd

import core
from core import validate
import models

st.set_page_config(layout="wide")


data_loader = st.cache(allow_output_mutation=True)(core.load_data)
if "data" not in st.session_state:
    df = data_loader()
    df = df.set_index("id", drop=False)
    st.session_state["data"] = df
else:
    df = st.session_state["data"]


rows = validate.apply_warnings(df)
rows_with_warnings = pd.DataFrame(rows)
if not rows_with_warnings.empty:
    rows_with_warnings = rows_with_warnings.set_index("id")
    count = rows_with_warnings.sum(axis=1)
    df["Warnings"] = count
else:
    df["Warnings"] = 0

rows = validate.apply_business_rules(df)
failed_rows = pd.DataFrame(rows)
if not failed_rows.empty:
    failed_rows = failed_rows.set_index("id")
    print(failed_rows)
    count = failed_rows.sum(axis=1)
    print(count)
    df["Failed_Business_Rules"] = count
else:
    df["Failed_Business_Rules"] = 0



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
print("SHITTTTT\n", df)

grid_response: models.GridResponse = st_aggrid.AgGrid(
    data=df,
    height=500,
    gridOptions=gb.build(),
    width='100%',
    columns_auto_size_mode=st_aggrid.ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
    update_on=[("cellValueChanged", 100)],
    data_return_mode=st_aggrid.DataReturnMode.FILTERED_AND_SORTED,
)

st.markdown("## Rows that failed business rules")
st.dataframe(failed_rows)

st.markdown("## Rows with warnings")
st.dataframe(rows_with_warnings)

df = grid_response['data']
print("SHITTTTT\n", df)
df["valid_from"] = pd.to_datetime(df["valid_from"], format="%Y-%m-%dT%H:%M:%S.%")
df["valid_until"] = pd.to_datetime(df["valid_until"], format="%Y-%m-%dT%H:%M:%S.%")
st.session_state["data"] = df.set_index("id", drop=False)

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