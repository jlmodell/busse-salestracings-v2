from s3_storage import CLIENT, S3_BUCKET


def GET_FIELDS_FILE(prefix: str, key: str) -> str:
    field_file = CLIENT.get_object(
        Bucket=S3_BUCKET, Key=prefix + key)['Body'].read().decode('utf-8')

    return field_file
