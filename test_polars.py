import polars as pl
import pandas as pd

from arguments import *
from constants import *
from database import *
from s3_storage import *

from rich import print

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


if __name__ == "__main__":

    # prioritues
    print("states", len(STATES_AS_STR))
    print("zipcodes", len(ZIP_CODES_AS_STR))
    print("cardinal branches", len(CARDINAL_BRANCHES_AS_STR))
    print("custom kits", len(CUSTOM_KITS))

    def determine_sales_rep(
        state: str, zip_code: str, cardinal_branch: str, kit: str
    ) -> str:
        sales_rep = "Rep40"
        print(state, zip_code, cardinal_branch, kit)

        if state != "Rep40":
            sales_rep = state
            print(sales_rep)

        if zip_code != "Rep40":
            sales_rep = zip_code
            print(sales_rep)

        if cardinal_branch != "Rep40":
            sales_rep = cardinal_branch
            print(sales_rep)

        if kit != "Rep40":
            sales_rep = kit
            print(sales_rep)

        print(sales_rep)
        return sales_rep

    df = (
        pl.DataFrame(df)
        .lazy()
        .with_column(
            (
                pl.col("9")
                .apply(lambda x: STATES_AS_STR.get(x, "Rep40"))
                .alias("__rep__state__")
            )
        )
        .with_column(
            (
                pl.col("10")
                .apply(lambda x: ZIP_CODES_AS_STR.get(x[:3], "Rep40"))
                .alias("__rep__zipcode__")
            )
        )
        .with_column(
            (
                pl.col("4")
                .apply(lambda x: CARDINAL_BRANCHES_AS_STR.get(x, "Rep40"))
                .alias("__rep__branch__")
            )
        )
        .with_column(
            (
                pl.col("12")
                .apply(lambda x: CUSTOM_KITS.get(x, "Rep40"))
                .alias("__rep__kit__")
            )
        )
        .with_column(
            (
                (
                    pl.when(~pl.col("__rep__state__").str.contains(r"^Rep40$"))
                    .then(pl.col("__rep__state__"))
                    .otherwise("Rep40")
                ).alias("__rep__")
            )
        )
        .with_column(
            (
                (
                    pl.when(
                        (~pl.col("__rep__zipcode__").str.contains(r"^Rep40$"))
                        & (~pl.col("__rep__").str.contains(r"^Rep40$"))
                    )
                    .then(pl.col("__rep__zipcode__"))
                    .otherwise(pl.col("__rep__"))
                ).alias("__rep__")
            )
        )
        .with_column(
            (
                (
                    pl.when(
                        (~pl.col("__rep__branch__").str.contains(r"^Rep40$"))
                        & (~pl.col("__rep__").str.contains(r"^Rep40$"))
                    )
                    .then(pl.col("__rep__branch__"))
                    .otherwise(pl.col("__rep__"))
                ).alias("__rep__")
            )
        )
        .with_column(
            (
                (
                    pl.when(
                        (~pl.col("__rep__kit__").str.contains(r"^?!Rep40$"))
                        & (~pl.col("__rep__").str.contains(r"^Rep40$"))
                    )
                    .then(pl.col("__rep__kit__"))
                    .otherwise(pl.col("__rep__"))
                ).alias("__rep__")
            )
        )
        .select("*")
        .limit(1)
        .collect()
    )

    # df = (
    #     df.groupby(["__rep__", "12", "15"])
    #     .agg(
    #         [
    #             pl.col("14").sum().alias("quantity"),
    #             pl.col("16").sum().alias("sale_value"),
    #         ]
    #     )
    #     .sort("__rep__")
    # )

    df.write_csv("test.csv")

    print(df)
