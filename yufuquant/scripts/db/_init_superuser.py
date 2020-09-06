from users.models import User


def run():
    print("Creating admin user...")
    User.objects.create_superuser(
        username="admin", password="test123456", email="admin@yufuquant.cc"
    )
