from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class Rep(str, Enum):
    """
    Enum for the number of reps
    """
    rep1 = "Rep1"
    rep2 = "Rep2"
    rep3 = "Rep3"
    rep4 = "Rep4"
    rep5 = "Rep5"
    rep6 = "Rep6"
    rep7 = "Rep7"
    rep8 = "Rep8"
    rep9 = "Rep9"
    rep10 = "Rep10"
    rep11 = "Rep11"
    rep12 = "Rep12"
    rep13 = "Rep13"
    rep14 = "Rep14"
    rep15 = "Rep15"
    rep16 = "Rep16"
    rep17 = "Rep17"
    rep18 = "Rep18"
    rep19 = "Rep19"
    rep20 = "Rep20"
    rep21 = "Rep21"
    rep22 = "Rep22"
    rep23 = "Rep23"
    rep24 = "Rep24"
    rep25 = "Rep25"
    rep26 = "Rep26"
    rep27 = "Rep27"
    rep28 = "Rep28"
    rep29 = "Rep29"
    rep30 = "Rep30"

    house = "House"


class Distributor(str, Enum):
    """
    Enum for the number of distributors
    """
    default = "SALES_NON_TRACED"

    mckesson = "MCKESSON"
    cardinal = "CARDINAL"
    om = "OWENSMINOR"
    hs = "HENRYSCHEIN"
    medline = "MEDLINE"
    concordance = "CONCORDANCE"
    ndc = "NDC"


class Sale(BaseModel):
    sale_date: datetime = Field(..., description="The date of the sale")

    rep: Rep = Field(..., description="The rep that gets credit for the sale")
    distributor: Distributor = Field(...,
                                     description="The distributor that reported the sale")
    item: str = Field(..., description="The item")
    distributor_item: Optional[str] = Field(
        None, description="The item reported by the distributor")

    sale_amount: float = Field(..., description="The amount of the sale")
    quantity: int = Field(..., description="The quantity of the sale")
    uom: str = Field(..., description="The unit of measure")

    invoice_nbr: str = Field(..., description="The invoice number")
    period: str = Field(..., description="The period")
    created_at: datetime = Field(..., default_factory=datetime.now,
                                 description="The date the record was created")

    division: str = Field(
        ..., description="The distributor depot division or unique identifier for location")

    unique_identifier: Optional[str] = Field(
        None, description="The unique identifier")

    end_user_name: str = Field(..., description="The end user name")
    end_user_address: str = Field(..., description="The address of the sale")
    end_user_address_2: str = Field(..., description="The address of the sale")
    end_user_city: str = Field(..., description="The city of the sale")
    end_user_state: str = Field(..., description="The state of the sale")
    end_user_zip_code: str = Field(..., description="The zip code of the sale")

    contract: Optional[str] = Field(None, description="The contract number")
    rebate_amount: Optional[float] = Field(
        None, description="The rebate amount")

    class Config:
        use_enum_values = True
