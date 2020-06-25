from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from pydantic import validator


def _alias_gen(text: str) -> str:
    return text.replace("_", "-")


class UserType(Enum):
    plus_user = "plus_user"
    non_plus_user = "non_plus_user"


class BasePSModel(BaseModel):
    class Config:
        alias_generator = _alias_gen
        allow_population_by_field_name = True
        orm_mode = True


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
    release_date: datetime
    prices: ItemPrices
    user_type: UserType
    url: HttpUrl

    last_updated: Optional[datetime]

    @validator("last_updated", pre=True)
    def update_time(cls, v):
        return v or datetime.utcnow()

    @property
    def price(self) -> ItemPriceForUser:
        return (
            self.prices.non_plus_user
            if self.user_type is UserType.non_plus_user
            else self.prices.plus_user
        )

    @property
    def has_discount(self) -> bool:
        return self.price.discount_percentage > 0

    @property
    def is_released(self) -> bool:
        return self.release_date.date() <= datetime.utcnow().date()


class PSProfile(BasePSModel):
    online_id: str = Field(..., alias="onlineid")
    online_name: str = Field(..., alias="onlinename")
    about_me: str = Field(..., alias="aboutme")
    avatar_url: HttpUrl = Field(..., alias="avatarurl")
    medium_avatar_url: HttpUrl = Field(..., alias="medium_avatarurl")
    small_avatar_url: HttpUrl = Field(..., alias="small_avatarurl")
    clutsmall_avatar_url: HttpUrl = Field(..., alias="clutsmall_avatarurl")
    ps_plus: bool
