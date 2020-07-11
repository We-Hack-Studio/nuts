from users.models import User


def run():
    print("初始化生成管理员账户...")
    User.objects.create_superuser(
        username="admin", password="test123456", email="admin@yufuquant.cc"
    )
