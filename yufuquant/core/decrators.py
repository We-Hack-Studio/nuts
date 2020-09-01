import functools
import typing

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def field_whitelist(fields: typing.Iterable, raise_exception: bool = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # self.request
                request = args[0].request
            except AttributeError:
                # first arg is request
                request = args[0]

            extras = request.data.keys() - set(list(fields) + ["id"])
            if len(extras) != 0 and raise_exception:
                raise ValidationError(
                    {"detail": _("Only accept {fields} fields.".format(fields=fields))}
                )

            for black_field in extras:
                del request.data[black_field]
            return func(*args, **kwargs)

        # wrapper.__wrapped__ = func
        return wrapper

    return decorator
