from rest_framework import serializers
from . models import Recipe
from tag.models import Tag
from authors.validators import AuthorRecipeValidation


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=25)
    slug = serializers.SlugField()


# leia mais abaixo sobre o uso de ModelSerializer
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'is_published',
            'title',
            'description',
            'slug',
            'servings',
            'servings_unit',
            'preparation_steps',
            'preparation_steps_is_html',
            'preparation_time',
            'preparation_time_unit',
            'created_at',
            'updated_at',
            'cover',
            'category',
            'author',
            'tags',
            'tag_objects',
        ]

    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

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

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)

        AuthorRecipeValidation(data=attrs,
                               error_class=serializers.ValidationError)

        return super_validate


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
