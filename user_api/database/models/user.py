from tortoise import fields
from tortoise.models import Model

from user_api.database.helpers import MailingType


class User(Model):
    id = fields.UUIDField(pk=True)
    tg_id = fields.IntField(unique=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50, null=True)
    is_bot = fields.BooleanField()
    mailing_type = fields.IntEnumField(enum_type=MailingType, default=MailingType.standart_mailing)
    created_at = fields.DateField(generated=True)
    last_activity_date = fields.DateField(generated=True)
    is_active = fields.BooleanField(default=True)
    is_deleted = fields.BooleanField(default=False)

    class Meta:
        table = "users"