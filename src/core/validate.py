import collections
import datetime as dt

import cytoolz


def price_below_cost(row):
    if row["price"] < row["cost"]:
        return {"price_below_cost": True}


def price_equal_cost(row):
    if row["price"] == row["cost"]:
        return {"price_equal_cost": True}


def margin_too_low(row):
    if (row["price"] - row["cost"]) / row["price"] < 0.15:
        return {"margin_too_low": True}


def price_expired(row):
    if dt.datetime.combine(row["valid_until"], dt.datetime.min.time()) <= dt.datetime.now():
        return {"expired price": True}


@cytoolz.curry
def apply_rules(data: "pandas.DataFrame", rules):
    broken_rules_d = []
    for row in data.itertuples():
        d = row._asdict()
        broken_rules = [rule(d) for rule in rules]
        broken_rules = [rule for rule in broken_rules if rule is not None]

        if broken_rules:
            broken_rules_d.append(dict(collections.ChainMap({"id": d["id"]}, *broken_rules)))
    return broken_rules_d


apply_warnings = apply_rules(rules=[price_equal_cost, price_equal_cost])
apply_business_rules = apply_rules(rules=[price_expired, margin_too_low])
