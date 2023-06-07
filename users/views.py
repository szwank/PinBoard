import djoser.views
import rest_framework.permissions
from django.contrib.auth import (
    get_user_model,
)
from rest_framework import (
    status,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.response import (
    Response,
)

User = get_user_model()


class UserViewSet(djoser.views.UserViewSet):
    def get_permissions(self):
        if self.action == "activate_user":
            self.permission_classes = [rest_framework.permissions.AllowAny]
        return super().get_permissions()

    @action(
        methods=["get"], detail=False, url_path="activate_user/(?P<username>[^/.]+)"
    )
    def activate_user(self, request, username=None):
        """
        Endpoint activating user

        !!ATTENTION!!
        Normally this should be handled by sending email with activation link pointing to the get url
        where url is handled and post is send with parsed uid and token.
        This endpoint simulate this proces for an ease of required setup with email.
        This also helps with application exploration.

        Additionally, this is a bad design, get is updating database.
        """
        user = User.objects.filter(username=username).first()
        if not user:
            return Response(
                {"detail": {"user": f"User with name {username} not found"}},
                status=status.HTTP_404_NOT_FOUND,
            )
        user.is_active = True
        user.save()
        return Response({}, status=status.HTTP_200_OK)
