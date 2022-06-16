import os
from dotenv import load_dotenv

if os.environ["PRODUCTION"] == True:
    load_dotenv(os.path.join(os.environ["USERPROFILE"], ".env"))
else:
    load_dotenv(".env")

MONGODB_URI = os.environ.get('MONGODB_URI', None)
ACCESS_KEY = os.environ.get('ACCESS_KEY', None)
SECRET_KEY = os.environ.get('SECRET_KEY', None)
S3_URL = os.environ.get('S3_URL', None)
S3_BUCKET = os.environ.get('S3_BUCKET', None)

assert MONGODB_URI is not None, "MONGODB_URI is not set"
assert ACCESS_KEY is not None, "ACCESS_KEY is not set"
assert SECRET_KEY is not None, "SECRET_KEY is not set"
assert S3_URL is not None, "S3_URL is not set"
assert S3_BUCKET is not None, "S3_BUCKET is not set"
