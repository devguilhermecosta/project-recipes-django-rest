from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404  # noqa: F401
from django.db.models.query import QuerySet
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag
from ..permissions import IsOwner
import os


class RecipeApiV2Pagination(PageNumberPagination):
    page_size = int(os.environ.get('PAGE_SIZE', 2))


class RecipeApiV2View(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeApiV2Pagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        ]

    # permitir somente métodos específicos
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'options',
        'head',
    ]

    def get_object(self) -> Recipe:
        pk: int = self.kwargs.get('pk', '')

        obj: Recipe = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        qs: QuerySet = super().get_queryset(*args, **kwargs)

        query_params: dict = self.request.query_params

        category_id: str = query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        print('Query Strings: ', self.request.query_params)
        print('kwargs: ', self.kwargs)

        return qs

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs) -> Response:
        recipe: Recipe = self.get_object()
        serializer: RecipeSerializer = RecipeSerializer(
            instance=recipe,
            many=False,
            data=request.data,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author=request.user,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers,
                        )


@api_view()
def tag_api_detail(request: HttpRequest, pk: int) -> Response:
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk,
    )

    serializer: TagSerializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )

    return Response(serializer.data)
