import polars as pl
import pandas as pd

from arguments import *
from constants import *
from database import *
from s3_storage import *

from rich import print
from typing import List


def determine_sales_rep(row) -> str:
    state = row[0] == "Rep40"
    zip_code = row[1] == "Rep40"
    branch = row[2] == "Rep40"
    custom_kit = row[3] == "Rep40"

    sales_rep = "Rep40"

    if not state:
        sales_rep = row[0]
    if not zip_code:
        sales_rep = row[1]
    if not branch:
        sales_rep = row[2]
    if not custom_kit:
        sales_rep = row[3]

    return sales_rep


client = GET_CLIENT()
db = client.busse_sales_data_warehouse
dw = db.data_warehouse

docs = list(
    dw.find(
        {
            "__distributor__": "CARDINAL",
        },
        {
            "_id": 0,
        },
    )
)


df = pd.DataFrame(docs)


def credit_rep_from_cardinal_tracings(df: pd.DataFrame) -> pl.DataFrame:
    df = (
        pl.from_pandas(df)
        .lazy()
        .with_columns(
            (
                (
                    pl.col("9")
                    .apply(lambda x: STATES_AS_STR.get(x, "Rep40"))
                    .alias("__rep__state__")
                ),
                (
                    pl.col("10")
                    .apply(lambda x: ZIP_CODES_AS_STR.get(x[:3], "Rep40"))
                    .alias("__rep__zipcode__")
                ),
                (
                    pl.col("3")
                    .apply(lambda x: CARDINAL_BRANCHES_AS_STR.get(x, "Rep40"))
                    .alias("__rep__branch__")
                ),
                (
                    pl.col("12")
                    .apply(lambda x: CUSTOM_KITS.get(x, "Rep40"))
                    .alias("__rep__kit__")
                ),
            )
        )
        .select(
            [
                pl.all(),
                pl.concat_list(
                    [
                        pl.col("__rep__state__"),
                        pl.col("__rep__zipcode__"),
                        pl.col("__rep__branch__"),
                        pl.col("__rep__kit__"),
                    ]
                ).alias("__rep__list__"),
            ]
        )
        .drop(["__rep__state__", "__rep__zipcode__", "__rep__branch__", "__rep__kit__"])
        .select(
            [
                pl.all(),
                pl.col("__rep__list__").apply(determine_sales_rep).alias("__rep__"),
            ]
        )
        .drop("__rep__list__")
        .select("*")
        # .limit(20)
    )

    return df.collect()


def aggregate_by_rep(df: pl.DataFrame) -> pl.DataFrame:
    df = (
        df.lazy()
        .groupby(["__rep__", "12", "15"])
        .agg(
            [
                pl.col("14").sum().alias("quantity"),
                pl.col("16").sum().alias("sale_value"),
            ]
        )
        .sort("__rep__")
    )

    return df.collect()


if __name__ == "__main__":

    # priorities
    # print("states", len(STATES_AS_STR))
    # print("zipcodes", len(ZIP_CODES_AS_STR))
    # print("cardinal branches", len(CARDINAL_BRANCHES_AS_STR))
    # print("custom kits", len(CUSTOM_KITS))

    cardinal = aggregate_by_rep(credit_rep_from_cardinal_tracings(df))

    cardinal.write_csv("cardinal.csv")

    print(cardinal)
