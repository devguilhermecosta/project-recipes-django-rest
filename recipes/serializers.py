from rest_framework import serializers
from . models import Recipe


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

    def any_method_name(self, recipe: Recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
