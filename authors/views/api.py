from authors.serializer import AuthorSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model


# < criar as urls do author no Insomina para testar >


# Criando a classe author que permite somente leitura:
#
# Criar a classe herdando de ReadOnlyModelViewSet
# Isso faz com que as views sejam somente de leitura
# Na queryset devemos retornar somente o usuário cujo
# username seja o mesmo da requisição.
# Isso obriga o usuário estar logado para ver seus
# próprios dados.
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

    @action(
        methods=['get'],
        detail=False,
    )
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj,
        )
        return Response(
            serializer.data
        )

# Criando uma url personalizada para o router:
# O nome do método será o mesmo da url, então,
# escolha bem o nome do método.
# Este método deverá ser decorado com @action.
# Se for uma url de detalhes, o atributo
# detail deverá ser True (quando isso ocorrer,
# um pk deverá ser passado como um atributo para
# a url).
# Exemplo:
#
# @action(
#     methods=['get'],
#     detail=False,
#       )
# def me(self, request, *args, **kwargs):
#     obj = self.get_queryset().first()
#     serializer = self.get_serializer(
#         instance=obj,
#     )
#     return Response(
#         serializer.data
#     )
