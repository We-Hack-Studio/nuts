from robots.serializers import PercentageField


def test_percentage_field_to_representation():
    field = PercentageField()
    assert field.to_representation(1), "100.00%"
    assert field.to_representation(0.0), "0.00%"
    assert field.to_representation(0.01), "1.00%"
    assert field.to_representation(0.001), "0.10%"
