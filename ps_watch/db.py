from datetime import datetime

from pony.orm import Database
from pony.orm import Json
from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Set

from ps_watch.models import UserType

db = Database()


class DBPSItem(db.Entity):
    id = PrimaryKey(str)
    name = Required(str)
    description = Required(str)
    release_date = Required(datetime)
    prices = Required(Json)
    user_type = Set(UserType.__members__.keys())
    url = Required(str)

    added_on = Required(datetime, default=datetime.utcnow)
    updated_on = Optional(datetime)


db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
