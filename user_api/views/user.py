from datetime import date

from pydantic import BaseModel

from user_api.database.helpers import MailingType


class UserView(BaseModel):
    tg_id: int
    first_name: str
    last_name: str | None = None
    is_bot: bool
    mailing_type: MailingType | None = None
    created_at: date | None = None
    last_activity_date: date | None = None
    is_active: bool | None = None
    is_deleted: bool | None = None
    
