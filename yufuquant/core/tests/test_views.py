from core.views import exception_handler
from rest_framework.exceptions import APIException


class TestExceptionHandler:
    def test_response_data_is_list(self):
        exc = APIException("error message")
        response = exception_handler(exc, {})
        assert response.data == ["error message"]

    def test_response_data_is_dict_and_has_detail_key(self):
        exc = APIException({"detail": "error message"})
        response = exception_handler(exc, {})
        assert response.data == ["error message"]

    def test_response_data_is_serializer_validation_error(self):
        exc = APIException({"url": ["error message"]})
        response = exception_handler(exc, {})
        assert response.data == {"url": ["error message"]}
