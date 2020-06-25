from functools import partial
from string import Template
from typing import List
from typing import Optional
from typing import Tuple

from httpx import Client
from httpx import ConnectTimeout
from httpx import HTTPError

from ps_watch.exceptions import PSWatchAPIError
from ps_watch.models import PSItem
from ps_watch.models import PSProfile
from ps_watch.models import UserType
from ps_watch.utils import glom
from ps_watch.utils import serialize

BASE_URL = "https://store.playstation.com"
PROFILE_URL = f"{BASE_URL}/kamaji/api/valkyrie_storefront/00_09_000/user/profile"
LIST_URL = f"{BASE_URL}/kamaji/api/valkyrie_storefront/00_09_000/gateway/lists/v1/users/me/lists"

ITEMS_URL_TEMPLATE = Template(f"{LIST_URL}/$list_id/items")
ITEM_URL_TEMPLATE = Template(f"{BASE_URL}/valkyrie-api/$locale/19/resolve/$item_id")
ITEM_STORE_URL_TEMPLATE = Template(f"{BASE_URL}/$locale/product/$item_id")


class PSStoreAPI:
    """
    Class representing the PS Store API
    """

    def __init__(
        self,
        locale: Tuple[str, str] = ("en", "US"),  # todo add support for other locales
        client: Optional[Client] = None,
        user_type: UserType = UserType.non_plus_user,
    ):
        self.locale = locale
        self.client = client or Client()
        self.user_type = user_type

    @property
    def api_locale(self) -> str:
        return "/".join(self.locale)

    @property
    def store_locale(self) -> str:
        return "-".join(self.locale).lower()

    def get(
        self, url: str, session_id: Optional[str] = None, to_json: bool = True, **kwargs
    ) -> dict:
        """A helper method to handle API get requests"""
        if session_id:
            self.client.cookies["JSESSIONID"] = session_id
        try:
            rsp = self.client.get(url, **kwargs)
            rsp.raise_for_status()
            return rsp.json() if to_json else rsp
        except (HTTPError, ConnectTimeout) as e:
            raise PSWatchAPIError(e)

    def get_wish_list_id(self, session_id: str) -> str:
        params = {"listTypes": "WISHLIST"}
        lists = self.get(url=LIST_URL, session_id=session_id, params=params)
        return glom(lists, "lists.0.listId")

    def get_list_item_ids(
        self, list_id: str, session_id: str, limit: int = 20
    ) -> List[str]:
        items_url = ITEMS_URL_TEMPLATE.substitute(list_id=list_id)
        params = {"limit": limit, "offset": 0, "sort": "-addTime"}

        raw_items = []
        item_get_func = partial(
            self.get, items_url, session_id=session_id, params=params
        )

        raw_rsp = item_get_func()
        while raw_rsp["totalItems"] >= raw_rsp["returned"] > 0:
            raw_items += raw_rsp["items"]
            params["offset"] += raw_rsp["returned"]
            raw_rsp = item_get_func()

        return glom(raw_items, ["itemId"])

    def get_item(self, item_id: str) -> PSItem:
        api_url = ITEM_URL_TEMPLATE.substitute(locale=self.api_locale, item_id=item_id)
        store_url = ITEM_STORE_URL_TEMPLATE.substitute(
            locale=self.store_locale, item_id=item_id
        )
        raw_data = self.get(api_url)
        first_item = glom(raw_data, "included.0")
        item_spec = {
            "name": "attributes.name",
            "description": "attributes.long-description",
            "id": "id",
            "prices": "attributes.skus.0.prices",
            "release_date": "attributes.release-date",
        }
        item_data = glom(first_item, item_spec)
        return serialize(
            PSItem,
            item_data,
            user_type=self.user_type,
            api_url=api_url,
            store_url=store_url,
        )

    def get_items(self, item_ids: List[str]) -> List[PSItem]:
        return [self.get_item(item_id) for item_id in item_ids]

    def get_user_profile(self, session_id: str) -> PSProfile:
        profile = self.get(PROFILE_URL, session_id=session_id)
        return serialize(PSProfile, profile["data"])

    def update_user_type(self, session_id: str):
        profile = self.get_user_profile(session_id)
        self.user_type = (
            UserType.plus_user if profile.ps_plus else UserType.non_plus_user
        )

    def get_items_from_wish_list(self, session_id: str) -> List[PSItem]:
        wish_list_id = self.get_wish_list_id(session_id)
        item_ids = self.get_list_item_ids(wish_list_id, session_id)
        return self.get_items(item_ids)
