from credentials.models import Credential
from django.conf import settings
from django.contrib.auth import get_user_model
from exchanges.models import Exchange
from robots.models import Robot
from strategies.models import Strategy

User = get_user_model()


def run():
    if not settings.DEBUG:
        alert = (
            "You are not in development environment. "
            "This script will DELETE ALL DATA in your database. "
            "If you really want to continue this script, please input 'yEs'. "
            "Make sure you know what you are doing!"
        )
        print(alert)
        prompt = input("Please input 'yEs' to continue")
        if prompt != "yEs":
            print("Unexpected input, return!")
            return

    User.objects.all().delete()
    Exchange.objects.all().delete()
    Credential.objects.all().delete()
    Strategy.objects.all().delete()
    Robot.objects.all().delete()
    print("Database was cleaned.")
