from rest_framework import serializers
from . models import Recipe, Category
from tag.models import Tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=25)
    slug = serializers.SlugField()


# leia mais abaixo sobre o uso de ModelSerializer
class RecipeSerializer(serializers.Serializer):
    """
        OBSERVAÇÃO IMPORTANTE:

        Ao permitir a criação de novos objetos, temos a possibilidade
        de permitir que alguns atributos de classe sejam somente
        do tipo 'leitura', isto é, o usuário não poderá enviar este
        campo preenchido para o back-end.
        Para todo field que desejamos ser somente leitura, adicionar o
        atributo 'read_only=True',
        Qualquer field aceita este argumento.

    """

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)

    """
    Como renomear o field do model.
    Vamos usar como exemplo o field is_published.
    Usar o atributo 'source' para referenciar o field original
    """
    public = serializers.BooleanField(source='is_published')

    """
    Como unir dois ou mais fields em um único e novo field.
    Criar um método com o nome get_<nome_do_novo_field>.
    Exemplo: get_preparation.
    Você pode colocar qualquer nome usando o atributo method_name.
    """
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        )

    """
    Serializando fields do tipo foreingkey.
    Usamos o método PrimaryKeyRelatedField.
    Esse método recebe como atributo uma queryset.
    Ele retorna por padrão o pk de cada objeto.
    Isso pode ou não ser interessante para a aplicação.
    Uma opção para modificar isso é criar uma nova variável
    de classe sendo uma instância de StringRelatedField e usar
    o atributo 'source'. Isso funcionará se o field do model
    tiver um método __str__ implementado. Isso retornará um item
    json com category e outro category_name.
    Agora, se a intenção for retornar somente o __str__,
    basta usar uma instância de StringRelatedField sem source
    e de mesmo nome do field do model.
    Ex.: category = serilizers.StringRelatedField()
    """
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    category_name = serializers.StringRelatedField(
        source='category'
    )

    author = serializers.StringRelatedField()

    """
    Serializando objetos com relationship type many-to-many.
    Serializamos o field com PrimaryKeyRelatedField.
    Deve receber como atributos uma queryset e many=True.

    Uma opção para tornar mais intuitivo é criar uma
    classe para serializar cada tag.
    Então criamos um novo field que será uma instância
    da nova classe, passando o source e many como atributos.

    Ex.:
      class RecipeSerializer(serializers.Serializer):
          id = serializers.IntegerField()
          title = serializers.CharField(max_length=65)
          description = serializers.CharField(max_length=165)

      tag_objects = TagSerializer(
          source='tags',
          many=True,
      )
    """
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        default='',
    )
    tag_objects = TagSerializer(
        source='tags',
        many=True,
        default='',
    )

    """
    Criando links para as nossas tags.
    Podemos querer ter links para objetos relacionas em nossa API.
    Par isso, vamos seguir o passo a passo.

    1 - criar uma instância de HyperlinkdRelatedFiedl.

    2 - essa instância deve receber os seguintes atributos:
      a - queryset;
      b - many;
      c - source;
      d - view_name: deve ser o reverse para a view que leva até a tag,
      por exemplo: 'reccipes:api_v2_tag';

    3 - criar a url para a tag:
      exemplo:
          path('recipes/api/v2/tag/<int:pk>/',
              views.tag_api_detail,
              name='api_v2_tag',
              ),

    4 - criar a view para a url:
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

    5 - na view principal que renderiza TODAS as recipes, precisamos
        adicionar um atributo context no serializer:

          serializer = RecipeSerializer(
              instance=recipes,
              many=True,
              context={'request': request},
              )
    """
    tag_links = serializers.HyperlinkedRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        source='tags',
        view_name='recipes:api_v2_tag',
        default='',
    )

    def any_method_name(self, recipe: Recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    """
    Validando dados do serializer:
    - A validação funciona como a validação dos models do Django.
    - Podemos ter um método chamado 'validate', usado para validar
      um campo que depende do outro, e podemos usar os métodos
      validate_<nome_do_field> para validar um fild individual.
    - Quando usado 'validate', não é preciso usar um defaultdict
      para mapear os erros, mas sim criar um dicionário com os erros
      por field como valor de serializers.ValidationError.
    - Por fim, o ValidationError a ser usado deve partir de serializers,
      e o valor de cada chave deve ser uma lista e não string, pois
      podemos adicionar vários erros na mesma chave.
    """
    def validate(self, attrs):
        super_validate = super().validate(attrs)

        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError(
                {
                    "title": ["o título não pode ser igual a descrição"],
                    "description":
                        ["a descrição não pode ser igual ao título"],
                }
            )

        return super_validate

    def validate_title(self, value):
        title = value

        if len(title) < 5:
            raise serializers.ValidationError(
                'O título precisa ter pelo menos 5 caracteres.'
            )

        if title == 'qualquer coisa':
            raise serializers.ValidationError(
                "o título não pode ser 'qualquer coisa'."
            )

        return title


"""
    Herdando de serializers.ModelSerializer

    Quando uma classe herda de ModelSerializer, isso nos poupa
    de reescrever os fields já prontos no model.
    O seu uso é muito simples:

    1 - Declarar uma class Meta contendo o atributo de classe
        'model' e 'fields'.
        Embora em 'fields' seja possível o uso do valor __all__,
        não recomendo isso, pois podemos expor dados não desejados;

    2 - Fields do tipo PrimaryKeyRelatedField, isto é, fields do model
        do tipo ForeingKey, não precisam ser redeclarados, a menos
        que desejamos renomear o field;

    3 - Ao criar fields personalizados, os mesmos devem ser adicionados
        no atribudo de classe 'fields' na ordem que desejamos que sejam
        exibidos no front-end.

class RecipeSerializer(serializers.ModelSerializer):  # noqa: E302
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'public',
            'preparation',
            'category_name',
            'author',
            'tag_objects',
            'tag_links',
        ]

    public = serializers.BooleanField(source='is_published')

    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        )

    category_name = serializers.StringRelatedField(
        source='category'
    )

    author = serializers.StringRelatedField()

    tag_objects = TagSerializer(
        source='tags',
        many=True,
    )

    tag_links = serializers.HyperlinkedRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        source='tags',
        view_name='recipes:api_v2_tag',
    )

    def any_method_name(self, recipe: Recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
"""
