import datetime as dt
import collections

import cytoolz
from prefect import flow, task

from src import core


def margin_too_low(row):
    if (row["price"] - row["cost"]) / row["price"] < 0.15:
        return {"margin_too_low": True}


def price_expired(row):
    if dt.datetime.combine(row["valid_until"], dt.datetime.min.time()) <= dt.datetime.now():
        return {"expired price": True}


# @task
def apply_rules(data: "pandas.DataFrame"):
    rules = [price_expired, margin_too_low]
    broken_rules_d = []
    for row in data.itertuples():
        d = row._asdict()
        broken_rules = [rule(d) for rule in rules]
        broken_rules = [rule for rule in broken_rules if rule is not None]

        if broken_rules:
            broken_rules_d.append(dict(collections.ChainMap({"id": d["id"]}, *broken_rules)))
    return broken_rules_d



def price_below_cost(row):
    if row["price"] < row["cost"]:
        return {"price_below_cost": True}


def price_equal_cost(row):
    if row["price"] == row["cost"]:
        return {"price_equal_cost": True}


# @task
def apply(data: "pandas.DataFrame", rules):
    broken_rules_d = []
    for row in data.itertuples():
        d = row._asdict()
        broken_rules = [rule(d) for rule in rules]
        broken_rules = [rule for rule in broken_rules if rule is not None]

        if broken_rules:
            broken_rules_d.append(dict(collections.ChainMap({"id": d["id"]}, *broken_rules)))
    return broken_rules_d


# @flow(name="validate_pricing_data")
def validate_pricing_data(data):
    failed_rules = apply(data, rules=[price_expired, margin_too_low])
    warnings = apply(data, rules=[price_equal_cost, price_equal_cost])
    return failed_rules, warnings


if __name__ == '__main__':
    import timeit
    data = core.load_data()
    start = timeit.default_timer()
    fails, warnings = validate_pricing_data(data)
    print(timeit.default_timer() - start)
    print(warnings)

# todo
