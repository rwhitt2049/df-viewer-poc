import pandas as pd
import numpy as np
import random
import faker
import datetime as dt


random.seed(10)
faker.Faker.seed(10)
FAKE = faker.Faker()


def id_range(n):
    return tuple(f"P{i:03}" for i in range(n))


def load_data():
    data = []
    ids = id_range(25_000)

    for id_ in ids:
        price = random.randint(10, 10_000)
        cost = int(price * 0.83)
        data.append(
            {
                "id": id_,
                "price": np.float32(price / 100),
                "valid_from": FAKE.date_between(dt.datetime(2022, 1, 1), dt.datetime(2022, 10, 31)),
                "valid_until":  FAKE.date_between(dt.datetime(2022, 10, 1), dt.datetime(2023, 1, 1)),
                "cost": np.float32(cost / 100),
            }
        )

    df = pd.DataFrame(data)
    return df.set_index("id", drop=False)


#
# def high_light_failed(s):
#     return ["background-color: green"] * len(s) if s["Is valid"] else ["background-color: red"] * len(s)
#
#
# def load():
#     if "df" not in st.session_state:
#         st.session_state["data"] = DF
#     st.dataframe(st.session_state["data"])
#
#
# def validate():
#     """breaks if trying to validate but no data loaded"""
#     df = st.session_state["data"]
#     df["Is valid"] = df.price > 2
#     if "validated_date" not in st.session_state:
#         st.session_state.validated_date = df
#     st.dataframe(df.style.apply(high_light_failed, axis=1))
#
#
# # st.button("Load CSV", on_click=load)
# # st.button("Validate", on_click=validate)
#
# add_load = st.sidebar.button("Load CSV", on_click=load)
# add_validate = st.sidebar.button("Validate", on_click=validate)

