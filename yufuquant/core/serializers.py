from rest_framework import serializers


class MaskedCharField(serializers.CharField):
    def __init__(self, **kwargs):
        self.head_len = kwargs.pop("head_len", 4)
        self.tail_len = kwargs.pop("tail_len", 4)
        self.mask_all = kwargs.pop("mask_all", False)
        super().__init__(**kwargs)

    def to_representation(self, value):
        value = super().to_representation(value)
        if not value:
            return value

        if self.mask_all:
            return "*" * len(value)

        head = value[: self.head_len]
        hidden = value[self.head_len : -self.tail_len]
        tail = value[-self.tail_len :]
        return head + "*" * len(hidden) + tail
