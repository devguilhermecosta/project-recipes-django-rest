from rest_framework.test import APITestCase
from rest_framework.utils.serializer_helpers import ReturnList
from django.urls import reverse
from django.http import HttpResponse
from .test_recipe_base import RecipeMixin
from unittest.mock import patch
from recipes.models import Recipe, Category


class RecipeAPITests(APITestCase, RecipeMixin):
    def make_reverse(self) -> str:
        return reverse(
            'recipes:recipe-api-list'
        )

    def make_get_request(self, **kwargs) -> HttpResponse:
        aditional_url: str = kwargs.pop('page', '')
        return self.client.get(
            self.make_reverse() + aditional_url
        )

    def test_recipe_api_list_url_is_correct(self) -> None:
        url: str = self.make_reverse()

        self.assertEqual(
            url,
            '/recipes/api/v2/',
        )

    def test_recipe_api_list_returns_status_code_200(self) -> None:
        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.status_code,
            200,
        )

    @patch('recipes.views.api.RecipeApiV2Pagination.page_size', new=3)
    def test_recipe_api_load_correct_quantity_of_recipes(self) -> None:
        number_of_recipes: int = 7
        self.make_recipe_in_batch(qty=number_of_recipes)
        response: HttpResponse = self.make_get_request()

        num_of_recipes_loaded: int = len(response.data.get('results'))
        total_recipes: int = response.data.get('count')

        self.assertEqual(
            num_of_recipes_loaded,
            3
        )
        self.assertEqual(
            total_recipes,
            number_of_recipes
        )

    @patch('recipes.views.api.RecipeApiV2Pagination.page_size', new=3)
    def test_recipes_api_is_paginated(self) -> None:
        self.make_recipe_in_batch(qty=10)

        response: HttpResponse = self.make_get_request(page='?page=2')

        number_of_loaded_recipes: int = len(response.data.get('results'))

        self.assertEqual(
            number_of_loaded_recipes,
            3,
        )

    def test_recipes_api_do_not_show_recipes_not_published(self) -> None:
        recipes: list = self.make_recipe_in_batch(qty=2)
        recipe_not_published: Recipe = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()

        response: HttpResponse = self.make_get_request()
        data: ReturnList = response.data.get('results')

        num_of_loaded_recipes: int = len(data)

        self.assertEqual(
            num_of_loaded_recipes,
            1,
        )

    @patch('recipes.views.api.RecipeApiV2Pagination.page_size', new=10)
    def test_recipes_api_returns_only_recipes_with_filtered_by_category(self) -> None:  # noqa: E501
        # created 10 recipes
        recipes: list = self.make_recipe_in_batch(qty=10)

        # created two categories
        category: Category = self.make_category(name='my category')
        other_category: Category = self.make_category(name='other category')

        # for each recipe we set a category
        for recipe in recipes:
            recipe.category = category
            recipe.save()

        # in recipe zero, we set a category 'other_category'
        only_one_recipe: Recipe = recipes[0]
        only_one_recipe.category = other_category
        only_one_recipe.save()

        # we search all recipes with the category 'category'
        response: HttpResponse = self.make_get_request(
            page=f'?category_id={category.id}'
        )
        data: ReturnList = response.data.get('results')

        # the results should be 9
        num_of_loaded_recipes: int = len(data)

        self.assertEqual(
            num_of_loaded_recipes,
            9,
        )
