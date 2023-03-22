from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status
from django.shortcuts import get_object_or_404  # noqa: F401
from django.http import Http404
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


"""
Criando uma FBV para retornar uma lista de objetos:

1 - Decoar a função com @api_view;
2 - Criar a QuerySet de objetos e filtros se necessário;
3 - Referenciar a QuerySet no seu respectivo serializer
    através do atributo 'instance';
4 - O serializer por padrão recebe como atributo um OBJETO
    e não uma QUERYSET. Em caso de QUERYSET, usar o atributo
    many=True;
5 - Retornar uma Response com serilizer.data como atributo;
"""
@api_view(http_method_names=['get', 'post'])  # noqa: E302
def api_recipes_list(request: HttpRequest) -> Response:

    match request.method:
        case 'GET':
            recipes = Recipe.objects.get_published()
            serializer = RecipeSerializer(
                instance=recipes,
                many=True,
                context={'request': request},
                )

            return Response(serializer.data)

        case 'POST':
            serializer = RecipeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        case _:
            raise Http404()


"""
Criando uma FBV para retornar um único objeto como detail:

Método 1 -> usando get_object_or_404:
    a - Decorar a função com @api_view;
    b - A Função deve receber como parâmetro, além da request,
        um id;
    c - Criar uma instância de get_object_or_404 e pk como filter;
    d - Serializar o objeto com o seu respectivo serializer.
        Como o serializer recebe um OBJETO por padrão, o único
        atributo requerido é instance; many não precisa ser usado;
    e - Retornar uma Response usando o 'serilizer.data' como atributo.

Método 2 -> personalizando o retorno:
    O método 1 por padrão já resolveria nosso problema.
    Mas, caso se tenha a necessida de retornar uma mensagem diferente
    ou um status code personalizado, podemos usar esse método.

    a - Decorar a função com @api_view;
    b - A Função deve receber como parâmetro, além da request,
        um id;
    c - Criar uma instância de Recipe.objetos.get_objetct(pk=pk).first();
    d - Serializar o objeto com o seu respectivo serializer.
        Como o serializer recebe um OBJETO por padrão, o único
        atributo requerido é instance; many não precisa ser usado;
    e - Se o objeto existir, retornar uma Response usando o
        'serializer.data' como atributo;
    f - Se o objeto não existir, retornar uma Responser, unsado como
        primeiro atributo um dicionário com par chaver e valor envolvidos
        por ASPAS DUPLAS com a mensagem desejada, e como segundo atributo
        o status code desejado e fornecido por
        from rest_framework import status, e então usar status.HTTP...,
        por exemplo:

            return Response({
                "details": "not found",
            }, status=status.HTTP_404_NOT_FOUND)
"""
@api_view(http_method_names=['get', 'patch', 'delete'])  # noqa: E302
def api_recipes_detail(request: HttpRequest, pk: int) -> Response:
    recipe: Recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk,
        )

    if request.method == 'GET':
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request},
            )
        return Response(data=serializer.data)

    elif request.method == 'PATCH':
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            partial=True,
            context={'request': request},
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            )

    elif request.method == 'DELETE':
        recipe.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
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
