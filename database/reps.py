from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from constants import BUSSE_SALES_REPS, BUSSE_SALES_REPS_COLLECTIONS, REPS
from database import GET_CLIENT, GET_DATABASE, GET_COLLECTION


def GET_REPS_COLLECTION():
    client = GET_CLIENT()
    db = GET_DATABASE(client, BUSSE_SALES_REPS)
    return GET_COLLECTION(db, BUSSE_SALES_REPS_COLLECTIONS[REPS])


class Rep(BaseModel):
    name: str = Field(..., description="Name of the sales rep")
    email: EmailStr = Field(..., description="Email of the sales rep")
    territory_name: str = Field(..., description="Territory of the sales rep")
    territories: List[str] = Field(...,
                                   description="Territories of the sales rep")
    territory_id: str = Field(..., description="Territory ID of the sales rep")
    territory_base: float = Field(...,
                                  description="Base amount for the sales rep's territory")
    start_date: datetime = Field(...,
                                 description="Start date of the sales rep")
    active: bool = Field(..., description="Is the sales rep active?")
    owens_minor: Optional[bool] = Field(...,
                                        description="Is OM tracing available for this rep?")


LIST_OF_REPS = {x["territory_name"]: Rep(
    **x) for x in list(GET_REPS_COLLECTION().find({}))}


# Rep1 = Rep(
#     name="Brent Hill",
#     email="bhill@busseinc.com",
#     territory_name="Rep1",
#     territories=["TX", "OK"],
#     territory_id="1",
#     start_date=datetime(2004, 2, 1),
#     territory_base=1_636_293.00,
#     active=True,
#     owens_minor=False,
# )

# Rep3 = Rep(
#     name="Steve Spicer",
#     email="sspicer@busseinc.com",
#     territory_name="Rep3",
#     territories=["MI"],
#     territory_id="3",
#     start_date=datetime(2014, 2, 1),
#     territory_base=550_000.00,
#     active=True,
#     owens_minor=False,
# )

# Rep5 = Rep(
#     name="Chris Cardinale",
#     email="ccardinale@busseinc.com",
#     territory_name="Rep5",
#     territories=["FL"],
#     territory_id="5",
#     start_date=datetime(2020, 10, 1),
#     territory_base=1_300_000.00,
#     active=True,
#     owens_minor=False,
# )

# Rep7 = Rep(
#     name="Chuck Phillips",
#     email="cphillips@busseinc.com",
#     territory_name="Rep7",
#     territories=["IL", "IN", "WI"],
#     territory_id="7",
#     start_date=datetime(2017, 10, 1),
#     territory_base=1_200_000.00,
#     active=True,
#     owens_minor=False,
# )

# Rep8 = Rep(
#     name="John Casey",
#     email="jcasey@busseinc.com",
#     territory_name="Rep8",
#     territories=["CT", "MN", "NH", "RI", "VT"],
#     territory_id="8",
#     start_date=datetime(2017, 10, 1),
#     territory_base=1_350_000.00,
#     active=True,
#     owens_minor=False,
# )

# Rep13 = Rep(
#     name="Dan Gildea",
#     email="dgildea@busseinc.com",
#     territory_name="Rep13",
#     territories=["MD", "DC", "PA"],
#     territory_id="13",
#     start_date=datetime(1998, 6, 1),
#     territory_base=1_300_000.00,
#     active=True,
#     owens_minor=True,
# )

# Rep14 = Rep(
#     name="Roz Bernstein",
#     email="rbernstein@busseinc.com",
#     territory_name="Rep14",
#     territories=["NJ"],
#     territory_id="14",
#     start_date=datetime(2012, 10, 1),
#     territory_base=292_771.00,
#     active=True,
#     owens_minor=True,
# )

# Rep15 = Rep(
#     name="Tom Ranck",
#     email="tranck@busseinc.com",
#     territory_name="Rep15",
#     territories=["NC", "VA"],
#     territory_id="15",
#     start_date=datetime(2014, 5, 1),
#     territory_base=1_489_074.00,
#     active=True,
#     owens_minor=False,
# )

# Rep22 = Rep(
#     name="Roz Bernstein",
#     email="rbernstein@busseinc.com",
#     territory_name="Rep22",
#     territories=["NY"],
#     territory_id="22",
#     start_date=datetime(2012, 10, 1),
#     territory_base=666_060.00,
#     active=True,
#     owens_minor=True,
# )

# Rep23 = Rep(
#     name="Zach Querci",
#     email="zquerci@busseinc.com",
#     territory_name="Rep23",
#     territories=["NY"],
#     territory_id="23",
#     start_date=datetime(1999, 1, 1),
#     territory_base=2_300_000.00,
#     active=False,
#     owens_minor=True,
# )

# Rep25 = Rep(
#     name="Steve Spicer",
#     email="sspicer@busseinc.com",
#     territory_name="Rep25",
#     territories=["PA", "OH", "VA", "KY", "IN"],
#     territory_id="25",
#     start_date=datetime(2014, 2, 1),
#     territory_base=1_740_516.00,
#     active=True,
#     owens_minor=False,
# )

# Rep28 = Rep(
#     name="David Wright",
#     email="dwright@busseinc.com",
#     territory_name="Rep28",
#     territories=["NY"],
#     territory_id="28",
#     start_date=datetime(1999, 1, 1),
#     territory_base=0.00,
#     active=True,
#     owens_minor=True,
# )

# Rep29 = Rep(
#     name="Chris Cardinale",
#     email="ccardinale@busseinc.com",
#     territory_name="Rep29",
#     territories=["GA"],
#     territory_id="29",
#     start_date=datetime(2020, 10, 1),
#     territory_base=950_000.00,
#     active=True,
#     owens_minor=False,
# )

# Rep41 = Rep(
#     name="Adam Lichtenbaum",
#     email="alichtenbaum@busseinc.com",
#     territory_name="Rep41",
#     territories=["NY", "NJ"],
#     territory_id="41",
#     start_date=datetime(2022, 8, 1),
#     territory_base=2_300_000.00,
#     active=False,
#     owens_minor=False,
# )

# REPS_DICT = {
#     "1": Rep1,
#     "3": Rep3,
#     "5": Rep5,
#     "7": Rep7,
#     "8": Rep8,
#     "13": Rep13,
#     "14": Rep14,
#     "15": Rep15,
#     "22": Rep22,
#     "23": Rep23,
#     "25": Rep25,
#     "28": Rep28,
#     "29": Rep29,
#     "41": Rep41,
# }
