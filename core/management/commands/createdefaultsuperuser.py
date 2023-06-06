from django.contrib.auth import (
    get_user_model,
)
from django.core.management import (
    BaseCommand,
)

User = get_user_model()


class Command(BaseCommand):
    """"""

    help = "Create default superuser."

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
