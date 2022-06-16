from s3_storage import S3_BUCKET, CLIENT, GET_BYTES, GET_HTML_STR


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
