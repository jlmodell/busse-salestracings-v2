from typing import Tuple, Dict
from typing import Tuple


from pymongo.collection import Collection

from database import GET_CLIENT, GET_DATABASE, GET_COLLECTION
from constants import BUSSE_SALES_REPS, KITS


def GET_KITS_COLLECTION() -> Collection:
    client = GET_CLIENT()
    db = GET_DATABASE(client, BUSSE_SALES_REPS)
    coll = GET_COLLECTION(db, KITS)

    return coll


def PARSE_KITS() -> Tuple[Dict[str, float], Dict[str, str]]:
    coll = GET_KITS_COLLECTION()
    kits = list(coll.find({}))

    commission_rates = {k['item']: k['rate'] for k in kits}
    FMcustomkits = {k['item']: k['rep'] for k in kits}

    return commission_rates, FMcustomkits


CUSTOM_KIT_COMMISSION_RATES, CUSTOM_KITS = PARSE_KITS()
