from authors.serializer import AuthorSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        user = get_user_model()
        qs = user.objects.filter(
            username=self.request.user.username
        )
        return qs
