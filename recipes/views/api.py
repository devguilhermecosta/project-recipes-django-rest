from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404  # noqa: F401
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag
import os


class RecipeApiV2Pagination(PageNumberPagination):
    page_size = int(os.environ.get('PAGE_SIZE', 2))


class RecipeApiV2View(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeApiV2Pagination


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
