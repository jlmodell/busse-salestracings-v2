from pydantic import BaseModel, validator
from typing import Optional


class TracingFile(BaseModel):
    tracing_file: Optional[str] = None
    tracing_month: Optional[str] = None
    tracing_year: Optional[str] = None

    class Config:
        validate_assignment = True

    @validator('tracing_file')
    def file_validator(cls, v):
        return v if v else "tracing_file.csv"

    @validator('tracing_month')
    def month_validator(cls, v):
        return v if v else "05"

    @validator('tracing_year')
    def year_validator(cls, v):
        return v if v else "2022"
