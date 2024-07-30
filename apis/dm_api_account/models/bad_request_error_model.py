from pydantic import BaseModel, StrictStr, Field, Extra
from typing import Optional, Dict, List


class BadRequestError(BaseModel):
    class Config:
        extra = Extra.forbid

    message: Optional[StrictStr] = Field(None, description='Client message')
    invalid_properties: Optional[Dict[str, List[StrictStr]]] = Field(
        None,
        alias='invalidProperties',
        description='Key-value pairs of invalid request properties',
    )