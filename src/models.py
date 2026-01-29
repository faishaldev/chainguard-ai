from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

class Transaction(BaseModel):
    hash: str
    from_addr: str = Field(..., alias="from")
    to_addr: str = Field(..., alias="to")
    value: str
    gas_used: int
    timestamp: int
    method: Optional[str] = None

class InputPayload(BaseModel):
    entity_type: Literal["wallet", "contract"]
    entity_id: str
    chain: str
    transactions: List[Transaction]

    @field_validator('entity_type')
    def validate_entity_type(cls, v):
        if v not in ('wallet', 'contract'):
            raise ValueError("entity_type must be 'wallet' or 'contract'")
        return v
