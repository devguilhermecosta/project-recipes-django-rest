from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from authors.validators import AuthorRecipeValidation


class RecipeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = '__all__'

        exclude = ['is_published',
                   'preparation_steps_is_html',
                   'author',
                   'slug',
                   ]

        widgets = {
            'preparation_time_unit': forms.Select(choices=(
                ('minuto(s)', 'minuto(s)'),
                ('hora(s)', 'hora(s)'),
                ('dia(s)', 'dias(s)')
                )
            ),
            'servings_unit': forms.Select(choices=(
                ('pessoa(s)', 'pessoa(s)'),
                ('porção', 'porção'),
                ('porções', 'porções'),
            )),
            'cover': forms.FileInput(attrs={
                'class': 'RF__image',
                }),
        }

    # também podemos criar as funções de validação indiviual por field
    def clean(self, *args, **kwargs) -> None:
        super_clean = super().clean(*args, **kwargs)

        AuthorRecipeValidation(data=self.cleaned_data,
                               error_class=ValidationError,
                               )

        return super_clean
