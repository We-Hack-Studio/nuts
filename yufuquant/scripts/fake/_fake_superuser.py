from users.models import User


def run():
    User.objects.create_superuser(
        username="admin", password="test123456", email="admin@yufuquant.cc"
    )
    print("Superuser 'admin' was created.")
