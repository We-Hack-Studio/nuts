from core.serializers import MaskedCharField


class TestMaskedCharField:
    def test_mask_all(self):
        value = "sensitive"
        field = MaskedCharField(mask_all=True)
        assert field.to_representation(value) == "*********"

    def test_empty_value(self):
        value = ""
        field = MaskedCharField()
        assert field.to_representation(value) == ""

    def test_mask_defaults(self):
        value = "sensitive"
        field = MaskedCharField()
        assert field.to_representation(value) == "sens*tive"

    def test_mask_head_len(self):
        value = "sensitive"
        field = MaskedCharField(head_len=2)
        assert field.to_representation(value) == "se***tive"

    def test_mask_tail_len(self):
        value = "sensitive"
        field = MaskedCharField(tail_len=2)
        assert field.to_representation(value) == "sens***ve"

    def test_mask_head_len_and_tail_len(self):
        value = "sensitive"
        field = MaskedCharField(head_len=2, tail_len=2)
        assert field.to_representation(value) == "se*****ve"
