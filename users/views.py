import djoser.views
import rest_framework.permissions
from django.contrib.auth import (
    get_user_model,
)
from django.shortcuts import (
    redirect,
)
from djoser.serializers import (
    UserCreatePasswordRetypeSerializer,
)
from rest_framework import (
    status,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.generics import (
    GenericAPIView,
)
from rest_framework.renderers import (
    TemplateHTMLRenderer,
)
from rest_framework.response import (
    Response,
)

from tasks.serializers import (
    EpicSerializer,
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


class NewAccount(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users/new_account.html"
    serializer_class = UserCreatePasswordRetypeSerializer
    swagger_schema = None

    def get(self, request):
        serializer = self.get_serializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        serializer.save(user=self.request.user)
        return redirect("core:index")
