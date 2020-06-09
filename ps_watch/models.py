import re
from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field
from pydantic import HttpUrl

camel_to_snake = re.compile(r"(?<!^)(?=[A-Z])")


def _alias_gen(text: str) -> str:
    text = text.replace("_", "-")
    return camel_to_snake.sub("_", text).lower()


class PSItemType(Enum):
    game = "game"
    game_related = "game-related"
    legacy_sku = "legacy-sku"


class PSGameContentType(Enum):
    full_game = "Full Game"
    add_on = "Add-On"


class PSGenre(Enum):
    racing = "Racing"


class PSPlatform(Enum):
    ps4 = "PS4"


class PSClassification(Enum):
    game = "GAME"
    premium_game = "PREMIUM_GAME"
    downloadable_game = "DOWNLOADABLE_GAME"
    add_on = "ADD-ON"
    bundle = "BUNDLE"
    map = "MAP"
    virtual_currency = "VIRTUAL_CURRENCY"
    NA = "NA"


###


class BasePSModel(BaseModel):
    class Config:
        alias_generator = _alias_gen
        extra = Extra.forbid


class PSItemRelationship(BasePSModel):
    id: str
    type: PSItemType


class PSItemRelationshipData(BasePSModel):
    data: List[PSItemRelationship]


class PSItemRelationships(BasePSModel):
    children: PSItemRelationshipData
    legacy_skus: PSItemRelationshipData = None


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
    value: Optional[float]


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
    exp_after_first_use: int = None


class PSPriceView(BasePSModel):
    display: str
    value: int


class PSPriceAvailability(BasePSModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class PSPrice(BasePSModel):
    actual_price: PSPriceView
    availability: PSPriceAvailability
    discount_percentage: int
    is_plus: bool
    strikethrough_price: Optional[PSPriceView]
    upsell_price: Optional[PSPriceView]


class PSPrices(BasePSModel):
    non_plus_user: PSPrice = None
    plus_user: PSPrice = None


class PSSKU(BasePSModel):
    entitlements: List[PSSKUEntitlement]
    id: str
    is_preorder: bool = None
    multibuy: Optional[str]
    name: str
    playability_date: Union[datetime, str] = None
    plus_reward_description: str = None
    prices: PSPrices


class PSStarRating(BasePSModel):
    score: Optional[float]
    total: Optional[int]


class PSUpsellInfo(BasePSModel):
    discount_percentage_difference: int
    display_price: str
    is_free: bool
    type: str


class PSParent(BasePSModel):
    id: str
    name: str
    thumbnail: HttpUrl
    url: HttpUrl


class PSContentDescriptor(BasePSModel):
    description: str
    name: str
    url: Optional[str]


class PSContentRating(BasePSModel):
    content_descriptors: List[PSContentDescriptor]
    content_interactive_element: list = []  # todo
    rating_system: str
    url: HttpUrl


class PSItemAttributes(BasePSModel):
    amortize_flag: bool = None
    bundle_exclusive_flag: bool = None
    charge_immediately_flag: bool = None
    charge_type_id: int = None
    credit_card_required_flag: int = None
    badge_info: PSBadgeInfo = None
    cero_z_status: PSCeroZStatus = None
    content_type: int = None
    content_rating: PSContentRating = None
    default_sku: bool = None
    default_sku_id: str = None
    dob_required: bool = None
    file_size: PSFileSize = None
    game_content_type: Union[PSGameContentType, str] = None
    genres: List[PSGenre] = []
    has_igc: bool = None
    is_igc_upsell: bool = None
    is_multiplayer_upsell: bool = None
    kamaji_relationship: str = None
    legal_text: str = None
    long_description: str = None
    macross_brain_context: str = None
    media_list: PSMediaList = None
    name: str
    nsx_confirm_message: Optional[str]
    parent: Union[PSParent, str] = None
    platforms: Union[List[PSPlatform], List[int]] = []
    plus_reward_description: str = None
    primary_classification: PSClassification = None
    provider_name: str = None
    ps_camera_compatibility: str = None
    ps_move_compatibility: str = None
    ps_vr_compatibility: str = None
    release_date: datetime = None
    secondary_classification: PSClassification = None
    skus: List[PSSKU] = []
    star_rating: PSStarRating = None
    subtitle_language_codes: list = None
    tertiary_classification: PSClassification = None
    thumbnail_url_base: HttpUrl = None
    top_category: str = None
    upsell_info: PSUpsellInfo = None
    voice_language_codes: list = None  # todo
    type: str = None
    season_pass_exclusive_flag: bool = None
    sku_availability_override_flag: bool = None
    sku_type: int = None


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
