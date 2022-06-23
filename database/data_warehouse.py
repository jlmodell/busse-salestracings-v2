import os
import re
import sys
import pandas as pd
import numpy as np
from rich import print

from constants import BUSSE_SALES_DATA_WAREHOUSE, BUSSE_SALES_DATA_WAREHOUSE_COLLECTIONS, DATA_WAREHOUSE
from database import GET_CLIENT, GET_DATABASE, GET_COLLECTION


def GET_DATA_WAREHOUSE_COLLECTION():
    client = GET_CLIENT()
    db = GET_DATABASE(client, BUSSE_SALES_DATA_WAREHOUSE)
    return GET_COLLECTION(db, BUSSE_SALES_DATA_WAREHOUSE_COLLECTIONS[DATA_WAREHOUSE])


def get_datatypes_from_file_before_creating_df(file_path: str, delimiter: str = ",", header: int = None, str_fields: list = []) -> dict:
    if re.search(r"\.xl(sx|sm|s)$", file_path, re.I):
        dtypes = dict(pd.read_excel(file_path, header=header).dtypes)
    elif re.search(r"\.(csv|txt)$", file_path, re.I):
        dtypes = dict(pd.read_csv(
            file_path, delimiter=delimiter, header=header).dtypes)

    for key in str_fields:
        if re.search(r"^(\d|\d{2})", key):
            dtypes[int(key)] = "str"
        else:
            dtypes[key] = "str"

    return dtypes


def create_raw_df_from_file(file_path: str, delimiter: str = ",", header: int = None, str_fields: list = []) -> pd.DataFrame:
    dtypes = get_datatypes_from_file_before_creating_df(
        file_path, delimiter, header, str_fields)

    print(dtypes)

    assert len(dtypes) > 0, "No columns found"

    if re.search(r"\.xl(s|sx|sm)$", file_path, re.I):
        df = pd.read_excel(file_path, header=header, dtype=dtypes)
    elif re.search(r"\.(csv|txt)$", file_path, re.I):
        df = pd.read_csv(file_path, delimiter=delimiter,
                         header=header, dtype=dtypes)

    return df


def clean_df_for_ingesting_to_data_warehouse(df: pd.DataFrame) -> pd.DataFrame:
    df.fillna("")
    df = df[df[df.columns[0]].notnull()].copy()
    df = df[df[df.columns[-1]].notnull()].copy()
    df = df[df[df.columns[0]] != ""].copy()

    df = df.replace(np.nan, "", regex=True).copy()

    df.columns = [str(x) for x in df.columns]

    return df


def clean_om_tracings(df: pd.DataFrame) -> pd.DataFrame:
    # ["SHIP QTY", "PART NBR", "REBATE    ", "INVOICE COST     "]

    df["SHIP QTY"] = df["SHIP QTY"].astype(int)
    df["INVOICE COST     "] = df.apply(
        lambda row: row["INVOICE COST     "] * row["SHIP QTY"], axis=1)
    df["PART NBR"] = df["PART NBR"].astype(str).str.lstrip("0").str.strip()
    df["REBATE    "] = df["REBATE    "].astype(float)

    return df


def INGEST_RAW_TRACING(file_path: str, period: str, **kwargs) -> None:
    """
    Ingests the raw tracing data from the given file path.
    """

    assert kwargs.get(
        "distributor", None) is not None, "'distributor' key is required within fields file"
    assert os.path.exists(file_path), "File path does not exist"
    assert re.match(r"^\d{4}-\d{2}$",
                    period), "Period must be in the format YYYY-MM"

    additional_fields = {
        "__file__": os.path.basename(file_path),
        "__period__": period,
        "__distributor__": kwargs.get("distributor"),
    }

    df = create_raw_df_from_file(file_path, delimiter=kwargs.get(
        "delimiter", ","), header=kwargs.get("header", 0), str_fields=kwargs.get("str_fields", []))

    df = clean_df_for_ingesting_to_data_warehouse(df)

    df.to_excel("testing.xlsx")

    if additional_fields["__distributor__"] == "OM":
        df = clean_om_tracings(df)

    df["__file__"] = additional_fields["__file__"]
    df["__period__"] = additional_fields["__period__"]
    df["__distributor__"] = additional_fields["__distributor__"]

    data_warehouse = GET_DATA_WAREHOUSE_COLLECTION()

    data_warehouse.delete_many(
        {"__distributor__": additional_fields["__distributor__"], "__period__": additional_fields["__period__"]})
    data_warehouse.insert_many(df.to_dict(orient="records"))

    # if kwargs.get('calc_sale_amount', None) is not None:
    #     s, q = kwargs.get('calc_sale_amount').split(";")
    #     sale_amount = kwargs.get("raw_fields_map", {}).get(s)
    #     quantity = kwargs.get("raw_fields_map", {}).get(q)

    #     try:
    #         df[sale_amount] = df.apply(
    #             lambda row: row[sale_amount] * row[quantity], axis=1)
    #     except:
    #         print(f"{sale_amount} is not a valid field")
    #         sys.exit(1)
