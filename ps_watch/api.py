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


BASE_URL = "https://store.playstation.com/"
PROFILE_URL = urljoin(BASE_URL, "kamaji/api/valkyrie_storefront/00_09_000/user/profile")
LIST_URL = urljoin(
    BASE_URL, "kamaji/api/valkyrie_storefront/00_09_000/gateway/lists/v1/users/me/lists"
)
ITEM_URL = urljoin(BASE_URL, "valkyrie-api/{}/19/resolve/")


class PSStoreAPI:
    """
    Class representing the PS Store API
    """

    def __init__(self, locale: str = "en/US", client: Optional[Client] = None):
        self.locale = locale
        self.client = client or Client()

    @staticmethod
    def _serialize(model: Type[Union[PSProfile, PSItem]], data: dict):
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
        url = f"{ITEM_URL.format(self.locale)}/{item_id}"
        raw_data = self.get(url)
        item_spec = {
            "name": "included.0.attributes.name",
            "description": "included.0.attributes.long-description",
            "id": "included.0.id",
            "prices": "included.0.attributes.skus.0.prices",
        }
        item_data = glom(raw_data, item_spec)
        return self._serialize(PSItem, item_data)

    def get_items(self, item_ids: List[str]) -> List[PSItem]:
        return [self.get_item(item_id) for item_id in item_ids]

    def get_user_profile(self, session_id: str) -> PSProfile:
        profile = self.get(PROFILE_URL, session_id=session_id)
        return self._serialize(PSProfile, profile["data"])


p = PSStoreAPI()
f = p.get_item("UP0006-CUSA05999_00-NFS1800000000001")
pass
