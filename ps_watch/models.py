from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


def _to_underscore(text: str) -> str:
    return text.replace("-", "_")


class PSItemType(Enum):
    game = "game"


class PSGameContentType(Enum):
    full_game = "Full Game"


class PSGenre(Enum):
    racing = "Racing"


class PSPlatform(Enum):
    ps4 = "PS4"


class PSClassification(Enum):
    game = "GAME"
    premium_game = "PREMIUM_GAME"
    NA = "NA"


###


class BasePSModel(BaseModel):
    class Config:
        alias_generator = _to_underscore


class PSItemRelationshipChild(BasePSModel):
    id: str
    type: PSItemType


class PSItemRelationshipChildren(BasePSModel):
    data: List[PSItemRelationshipChild]


class PSItemRelationships(BasePSModel):
    children: PSItemRelationshipChildren


class PSItemData(BasePSModel):
    relationships: PSItemRelationships


class PSUser(BasePSModel):
    discount_percentage: int
    is_plus: bool
    type: str


class PSBadgeInfo(BasePSModel):
    non_plus_user: PSUser
    plus_user: PSUser


class PSCeroZStatus(BasePSModel):
    is_allowed_in_cart: bool
    is_on: bool


class PSFileSize(BasePSModel):
    unit: str
    value: float


class PSMediaUrl(BasePSModel):
    url: HttpUrl


class PSMediaPromo(BasePSModel):
    images: List[PSMediaUrl]
    videos: List[PSMediaUrl]


class PSMediaList(BasePSModel):
    preview: List[PSMediaUrl]
    promo: PSMediaPromo
    screenshots: List[PSMediaUrl]


class PSSKUEntitlement(BasePSModel):
    duration: int
    exp_after_first_use: int


class PSPriceView(BasePSModel):
    display: str
    value: int


class PSPriceAvailability(BasePSModel):
    start_date: datetime
    end_date: datetime


class PSPrice(BasePSModel):
    actual_price: PSPriceView
    availability: PSPriceAvailability
    discount_percentage: int
    is_plus: bool
    strikethrough_price: Optional[PSPriceView]
    upsell_price: Optional[PSPriceView]


class PSPrices(BasePSModel):
    non_plus_user: PSPrice
    plus_user: PSPrice


class PSSKU(BasePSModel):
    entitlements: List[PSSKUEntitlement]
    id: str
    is_preorder: bool
    multibuy: str
    name: str
    playability_date: datetime
    plus_reward_description: str
    prices: PSPrices


class PSStarRating(BasePSModel):
    score: float
    rating: int


class PSUpsellInfo(BasePSModel):
    discount_percentage_difference: int
    display_price: str
    is_free: bool
    type: str


class PSItemAttributes(BasePSModel):
    badge_info: PSBadgeInfo
    cero_z_status: PSCeroZStatus
    content_type: int
    default_sku_id: str
    dob_required: bool
    file_size: PSFileSize
    game_content_type: PSGameContentType
    genres: List[PSGenre]
    has_igc: bool
    is_igc_upsell: bool
    is_multiplayer_upsell: bool
    kamaji_relationship: str
    legal_text: str
    long_description: str
    macros_brain_context: str
    media_list: PSMediaList
    name: str
    nsx_confirm_message: str
    parent: str
    platform: List[PSPlatform]
    plus_reward_description: str
    primary_classification: PSClassification
    provider_name: str
    ps_camera_compatibility: str
    ps_move_compatibility: str
    ps_vr_compatibility: str
    release_date: datetime
    secondary_classification: PSClassification
    skus: List[PSSKU]
    star_rating: PSStarRating
    subtitle_language_codes: list
    tertiary_classification: PSClassification
    thumbnail_url_base: HttpUrl
    top_category: str
    upsell_info: PSUpsellInfo
    voice_language_code: list


class PSItem(BasePSModel):
    attributes: PSItemAttributes
    id: str
    relationships: PSItemRelationships
    type: PSItemType


class PSItemWrapper(BasePSModel):
    data: PSItemData
    included: List[PSItem]


class PSProfile(BasePSModel):
    online_id: str = Field(..., alias="onlineid")
    online_name: str = Field(..., alias="onlinename")
    about_me: str = Field(..., alias="aboutme")
    avatar_url: HttpUrl = Field(..., alias="avatarurl")
    medium_avatar_url: HttpUrl = Field(..., alias="medium_avatarurl")
    small_avatar_url: HttpUrl = Field(..., alias="small_avatarurl")
    clutsmall_avatar_url: HttpUrl = Field(..., alias="clutsmall_avatarurl")
    ps_plus: bool
