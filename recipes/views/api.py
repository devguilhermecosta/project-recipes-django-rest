from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    )
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404  # noqa: F401
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


class RecipeApiV2Pagination(PageNumberPagination):
    page_size = 2


# class RecipeApiV2View(ListCreateAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeApiV2Pagination

class RecipeApiV2View(APIView):
    def get(self, request: HttpRequest) -> Response:
        recipes: Recipe = Recipe.objects.get_published()
        serializer: RecipeSerializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        serializer: RecipeSerializer = RecipeSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RecipeApiV2Details(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeApiV2Pagination

# class RecipeApiV2Details(APIView):
#     def get_recipe(self, pk: int) -> Recipe:
#         recipe: Recipe = get_object_or_404(
#             Recipe.objects.get_published(),
#             pk=pk,
#         )
#         return recipe

#     def get(self, request: HttpRequest, pk: int) -> Response:
#         recipe: Recipe = self.get_recipe(pk)
#         serializer: RecipeSerializer = RecipeSerializer(
#             instance=recipe,
#             many=False,
#             context={'request': request},
#         )
#         return Response(serializer.data)

#     def patch(self, request, pk: int, **kwargs) -> Response:
#         recipe: Recipe = self.get_recipe(pk)
#         serializer: RecipeSerializer = RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             context={'request': request},
#             partial=True,
#             many=False,
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_201_CREATED,
#         )

#     def delete(self, request: HttpRequest, pk: int) -> Response:
#         recipe: Recipe = self.get_recipe(pk)
#         recipe.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT,
#         )


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
