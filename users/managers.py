from django.contrib.auth.base_user import (
    BaseUserManager,
)


class UserManager(BaseUserManager):
    """Model manager for User model to use e-mail to authenticate"""

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields):
        """
        Create and save a User with the given email and password.
        :param email: User's email to save
        :param password: User's password to save
        :param extra_fields: User's extra fields to save
        :return: User instance
        """

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email: str, password: str, **extra_fields):
        """
        Create and save a regular User.
        :param email: User's email to save
        :param password: User's password to save
        :param extra_fields: User's extra fields to save
        :return: User instance
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if extra_fields.get("is_superuser") is True:
            raise ValueError(
                "User cannot have set is_superuser=True. "
                "To create superuser call create_superuser instead."
            )

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Create and save SuperUser.
        :param email: User's email to save
        :param password: User's password to save
        :param extra_fields: User's extra fields to save
        :return: User instance
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
