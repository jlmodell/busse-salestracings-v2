from arguments import *
from constants import *
from database import *
from s3_storage import *

from rich import print
from datetime import datetime
import json
import os

parser.add_argument('--func', type=str,
                    help='function to ingest raw tracing data')

if __name__ == "__main__":
    args = parser.parse_args()

    match args.func:
        case "INGEST_RAW_TRACING":
            assert args.file_path is not None, "file_path is required"
            assert args.period is not None, "period is required"
            assert args.fields_file is not None, "fields_file is required"

            ff = os.path.join(os.getcwd(), "Include",
                              "input", args.fields_file)

            assert os.path.exists(ff), "fields_file does not exist"

            with open(ff) as f:
                kwargs = json.loads(f.read())

            print(kwargs)

            INGEST_RAW_TRACING(file_path=args.file_path,
                               period=args.period, **kwargs)
