from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return

    data = response.data

    # ["error message"]
    if isinstance(data, list):
        return response

    # {"detail": "error message"}
    if data is not None and "detail" in data:
        response.data = [data["detail"]]

    """
    {
        "url": [
            "This field is required."
        ]
    }
    """
    return response
