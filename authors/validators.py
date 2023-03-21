from django.core.exceptions import ValidationError
from collections import defaultdict
from utils.numbers import is_positive_number


class AuthorRecipeValidation:
    def __init__(self, data, errors=None, error_class=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.error_class = ValidationError if error_class is None else error_class  # noqa: E501
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs) -> None:
        title: str = str(self.data.get('title'))
        description: str = str(self.data.get('description'))
        preparation_time = str(self.data.get('preparation_time'))
        servings = str(self.data.get('servings'))

        if len(title) < 15:
            self.errors['title'].append(
                'O título deve ter pelo menos 15 caracteres'
                )

        if title == description:
            self.errors['title'].append(
                'O título não pode ser igual à descrição.'
                )
            self.errors['description'].append(
                'A descrição não pode ser igual ao título'
            )

        if not is_positive_number(preparation_time):
            self.errors['preparation_time'].append(
                'O tempo de preparo deve ser maior que zero'
            )

        if not is_positive_number(servings):
            self.errors['servings'].append(
                'O número de porções deve ser maior que zero'
            )

        if self.errors:
            raise self.error_class(self.errors)
