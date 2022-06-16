from arguments import *
from constants import *
from database import *
from s3_storage import *

from rich import print
from datetime import datetime


if __name__ == "__main__":
    rep1 = Rep(name='Brent Hill', email='bhill@busseinc.com', territory_name='Rep1', territories=['TX', 'OK'], territory_id='1', territory_base=1636293.0, start_date=datetime(2004, 2, 1,
                                                                                                                                                                               0, 0), active=True, owens_minor=False)
    b = TracingFile().dict()

    print(b)
