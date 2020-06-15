from string import Template
from typing import List
from typing import Optional
from typing import Type
from typing import Union
from urllib.parse import urljoin

from glom import glom
from httpx import Client
from httpx import HTTPError
from pydantic import ValidationError

from ps_watch.exceptions import PSWatchAPIError
from ps_watch.exceptions import PSWatchValidationError
from ps_watch.models import PSItem
from ps_watch.models import PSProfile
from ps_watch.models import UserType

BASE_URL = "https://store.playstation.com"
PROFILE_URL = f"{BASE_URL}/kamaji/api/valkyrie_storefront/00_09_000/user/profile"
LIST_URL = f"{BASE_URL}/kamaji/api/valkyrie_storefront/00_09_000/gateway/lists/v1/users/me/lists"
ITEM_URL_TEMPLATE = Template("valkyrie-api/$locale/19/resolve/$item_id")


class PSStoreAPI:
    """
    Class representing the PS Store API
    """

    def __init__(
        self,
        locale: str = "en/US",
        client: Optional[Client] = None,
        user_type: UserType = UserType.non_plus_user,
    ):
        self.locale = locale
        self.client = client or Client()
        self.user_type = user_type

    @staticmethod
    def _serialize(model: Type[Union[PSProfile, PSItem]], data: dict, **kwargs):
        data.update(kwargs)
        try:
            return model.parse_obj(data)
        except ValidationError as e:
            raise PSWatchValidationError(e, data)

    def get(
        self, url: str, session_id: Optional[str] = None, **kwargs
    ) -> Optional[dict]:
        """A helper method to handle API get requests"""
        if session_id:
            self.client.cookies["JSESSIONID"] = session_id
        try:
            # todo pagination
            rsp = self.client.get(url, **kwargs)
            rsp.raise_for_status()
            return rsp.json()
        except HTTPError as e:
            raise PSWatchAPIError(e)

    def get_wish_list_id(self, session_id: str) -> str:
        params = {"listTypes": "WISHLIST"}
        lists = self.get(url=LIST_URL, session_id=session_id, params=params)
        return glom(lists, "lists.0.listId")

    def get_list_item_ids(self, list_id: str, session_id: str) -> List[str]:
        items_url = f"{LIST_URL}/{list_id}/items"
        params = {"limit": 50, "offset": 0, "sort": "-addTime"}
        items = self.get(items_url, session_id=session_id, params=params)
        return glom(items, ("items", ["itemId"]))

    def get_item(self, item_id: str) -> PSItem:
        item_url = urljoin(
            BASE_URL, ITEM_URL_TEMPLATE.substitute(locale=self.locale, item_id=item_id)
        )
        raw_data = self.get(item_url)
        item_spec = {
            "name": "included.0.attributes.name",
            "description": "included.0.attributes.long-description",
            "id": "included.0.id",
            "prices": "included.0.attributes.skus.0.prices",
            "release_date": "included.0.attributes.release-date",
        }
        item_data = glom(raw_data, item_spec)
        return self._serialize(PSItem, item_data, user_type=self.user_type)

    def get_items(self, item_ids: List[str]) -> List[PSItem]:
        return [self.get_item(item_id) for item_id in item_ids]

    def get_user_profile(self, session_id: str) -> PSProfile:
        profile = self.get(PROFILE_URL, session_id=session_id)
        return self._serialize(PSProfile, profile["data"])

    def update_user_type(self, session_id: str):
        profile = self.get_user_profile(session_id)
        self.user_type = (
            UserType.plus_user if profile.ps_plus else UserType.non_plus_user
        )
