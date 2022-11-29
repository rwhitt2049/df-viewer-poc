from typing import TypedDict

import pandas


class SelectedRowNodeInfo(TypedDict):
    nodeRowIndex: int
    nodeId: str


class SelectedRow(TypedDict):
    _selectedRowNodeInfo: SelectedRowNodeInfo
    # the rest of the keys aren't relevant yet


Selection = list[SelectedRow]


class GridResponse(TypedDict):
    data: "pandas.DataFrame"
    selected_rows: Selection
