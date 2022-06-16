import json
import pandas as pd
from datetime import datetime

from s3_storage import S3_BUCKET, CLIENT, GET_BYTES, GET_HTML_STR, GET_FIELDS_FILE, GET_DICT_FROM_JSON


def SAVE_DF_AS_EXCEL(df: pd.DataFrame, prefix: str, filename: str) -> None:
    data = GET_BYTES(df, filename)

    CLIENT.put_object(
        Bucket=S3_BUCKET,
        Key=prefix + filename,
        Body=data
    )


def SAVE_DF_AS_HTML(df: pd.DataFrame, prefix: str, filename: str) -> None:
    data = GET_HTML_STR(df)

    CLIENT.put_object(
        Bucket=S3_BUCKET,
        Key=prefix + filename,
        Body=data.encode('utf-8')
    )


def SAVE_FILE_TO_S3(prefix: str, key: str, data) -> None:
    CLIENT.put_object(
        Bucket=S3_BUCKET,
        Key=prefix + key,
        Body=data
    )


def UPDATE_FIELDS_FILE(prefix: str, key: str, **kwargs) -> None:
    fields_file = GET_FIELDS_FILE(prefix, key)
    fields_file_as_dict = GET_DICT_FROM_JSON(fields_file)
# make backup of old fields_file
    SAVE_FILE_TO_S3(
        prefix=prefix, key=f"backups/{datetime.now():%Y%m%d%H%M%S}_{key}", data=json.dumps(fields_file_as_dict))

# make changes here
    for key, value in kwargs.items():
        fields_file_as_dict[key] = value
# end changes here


# save new fields_file to s3
    SAVE_FILE_TO_S3(
        prefix=prefix, key=key, data=json.dumps(fields_file_as_dict))
