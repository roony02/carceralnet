from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@carceralnet.com",
                password="Admin12345!"
            )
            self.stdout.write("Admin créé")
        else:
            self.stdout.write("Admin existe déjà")
