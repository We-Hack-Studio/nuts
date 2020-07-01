from users.models import User


def run():
    print("初始化生成超级用户...")
    User.objects.create_superuser(
        username="yufu", password="yufu123456", email="yufu@yufu.com"
    )
