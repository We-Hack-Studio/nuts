from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = "^[a-zA-Z0-9]+$"
    message = "用户名只能为字母和数字的组合"


username_validators = [UsernameValidator()]
