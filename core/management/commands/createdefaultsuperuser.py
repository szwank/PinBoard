from django.contrib.auth import (
    get_user_model,
)
from django.core.management import (
    BaseCommand,
)

User = get_user_model()


class Command(BaseCommand):
    """
    Create default superuser for application.

    Use only in the development environment as this is not secure.
    """

    help = "Create default superuser. The user username: admin and password: admin"

    def handle(self, *args, **options):
        if User.objects.filter(username="admin").first():
            self.stdout.write("User with name admin already exists")
            return
        user_detail = {
            "username": "admin",
            "password": "admin",
            "email": "admin@admin.com",
            "first_name": "Piotrus",
            "last_name": "Pan",
            "is_active": True,
            "sex": "male",
        }
        User.objects.create_superuser(**user_detail)
        self.stdout.write("User with name admin created! To log in use password admin.")
