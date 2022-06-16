import json
from datetime import datetime

from s3_storage import SAVE_FILE_TO_S3
from fields import GET_FIELDS_FILE, DECODE_FIELDS_FILE


def UPDATE_FIELDS_FILE(prefix: str, key: str, **kwargs) -> None:
    fields_file = GET_FIELDS_FILE(prefix, key)
    fields_file_as_dict = DECODE_FIELDS_FILE(fields_file)
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
