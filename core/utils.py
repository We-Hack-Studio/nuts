from django.core import signing
from django.core.exceptions import ObjectDoesNotExist


class KeyHelper:
    salt = "fisher"

    @classmethod
    def make_key(cls, data):
        return signing.dumps(obj=data, salt=cls.salt)

    @classmethod
    def from_key(cls, key):
        try:
            data = signing.loads(key, salt=cls.salt)
            return data
        except (
            signing.SignatureExpired,
            signing.BadSignature,
            ObjectDoesNotExist,
        ):
            return
