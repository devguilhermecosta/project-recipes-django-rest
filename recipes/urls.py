from django.urls import path, include
from recipes import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

app_name: str = 'recipes'


recipes_api_v2_router = SimpleRouter()
recipes_api_v2_router.register(
     'recipes/api/v2',
     views.RecipeApiV2View,
)

urlpatterns = [
    path('', views.RecipeHomeBase.as_view(), name='home'),
    path('recipe/search/', views.RecipeSearch.as_view(), name='search'),
    path('recipe/tags/<slug:slug>/', views.RecipeTag.as_view(), name='tag'),
    path('recipe/<int:pk>/', views.RecipeDetailsView.as_view(), name='recipe'),
    path('recipe/category/<int:category_id>/',
         views.RecipeCategory.as_view(),
         name='category',
         ),
    path('recipes/api/v1/',
         views.RecipeListViewApi.as_view(),
         name='recipe_api',
         ),
    path('recipes/api/v1/<int:pk>/',
         views.RecipeListViewDetailsApi.as_view(),
         name='recipe_details_api',
         ),
    path('recipes/theory/', views.theory, name='theory'),
    path('recipes/api/v2/tag/<int:pk>/',
         views.tag_api_detail,
         name='api_v2_tag',
         ),
    path('recipes/api/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair',
         ),
    path('recipes/api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh',
         ),
    path('recipes/api/token/verify/',
         TokenVerifyView.as_view(),
         name='token_verify',
         ),
    path('', include(recipes_api_v2_router.urls)),
]
