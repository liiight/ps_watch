from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


def _alias_gen(text: str) -> str:
    return text.replace("_", "-")


class BasePSModel(BaseModel):
    class Config:
        alias_generator = _alias_gen
        allow_population_by_field_name = True


class ItemPrice(BasePSModel):
    display: str
    value: int


class PriceAvailability(BasePSModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class ItemPriceForUser(BasePSModel):
    actual_price: ItemPrice
    availability: PriceAvailability
    discount_percentage: int
    is_plus: bool


class ItemPrices(BasePSModel):
    plus_user: Optional[ItemPriceForUser]
    non_plus_user: Optional[ItemPriceForUser]


class PSItem(BaseModel):
    id: str
    name: str
    description: str
    prices: ItemPrices


class PSProfile(BasePSModel):
    online_id: str = Field(..., alias="onlineid")
    online_name: str = Field(..., alias="onlinename")
    about_me: str = Field(..., alias="aboutme")
    avatar_url: HttpUrl = Field(..., alias="avatarurl")
    medium_avatar_url: HttpUrl = Field(..., alias="medium_avatarurl")
    small_avatar_url: HttpUrl = Field(..., alias="small_avatarurl")
    clutsmall_avatar_url: HttpUrl = Field(..., alias="clutsmall_avatarurl")
    ps_plus: bool
