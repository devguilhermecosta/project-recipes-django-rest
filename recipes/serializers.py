from rest_framework import serializers
from . models import Recipe, Category
from tag.models import Tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=25)
    slug = serializers.SlugField()


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)

    # Como renomear o field do model.
    # Vamos usar como exemplo o field is_published.
    # Usar o atributo 'source' para referenciar o field original
    public = serializers.BooleanField(source='is_published')

    # Como unir dois ou mais fields em um único e novo field.
    # Criar um método com o nome get_<nome_do_novo_field>.
    # Exemplo: get_preparation.
    # Você pode colocar qualquer nome usando o atributo method_name.
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        )

    # Serializando fields do tipo foreingkey.
    # Usamos o método PrimaryKeyRelatedField.
    # Esse método recebe como atributo uma queryset.
    # Ele retorna por padrão o pk de cada objeto.
    # Isso pode ou não ser interessante para a aplicação.
    # Uma opção para modificar isso é criar uma nova variável
    # de classe sendo uma instância de StringRelatedField e usar
    # o atributo 'source'. Isso funcionará se o field do model
    # tiver um método __str__ implementado. Isso retornará um item
    # json com category e outro category_name.
    # Agora, se a intenção for retornar somente o __str__,
    # basta usar uma instância de StringRelatedField sem source
    # e de mesmo nome do field do model.
    # Ex.: category = serilizers.StringRelatedField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    category_name = serializers.StringRelatedField(
        source='category'
    )

    author = serializers.StringRelatedField()

    # Serializando objetos com relationship type many-to-many.
    # Serializamos o field com PrimaryKeyRelatedField.
    # Deve receber como atributos uma queryset e many=True.
    #
    # Uma opção para tornar mais intuitivo é criar uma
    # classe para serializar cada tag.
    # Então criamos um novo field que será uma instância
    # da nova classe, passando o source e many como atributos.
    #
    # Ex.:
    #   class RecipeSerializer(serializers.Serializer):
    #       id = serializers.IntegerField()
    #       title = serializers.CharField(max_length=65)
    #       description = serializers.CharField(max_length=165)
    #
    #   tag_objects = TagSerializer(
    #       source='tags',
    #       many=True,
    #   )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    tag_objects = TagSerializer(
        source='tags',
        many=True,
    )

    def any_method_name(self, recipe: Recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
