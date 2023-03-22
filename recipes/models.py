from django.contrib.auth.models import User
from django.db import models
from tag.models import Tag
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from project.settings import MEDIA_ROOT
from django.db.models import F, Value
from django.db.models.functions import Concat
from PIL import Image
from random import SystemRandom
import os
import string as st


class Category(models.Model):
    name = models.CharField(max_length=65,
                            verbose_name='Nome',
                            )

    def __str__(self) -> str:
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True,
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id').select_related('category', 'author')\
            .prefetch_related('tags')


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165,)
    slug = models.SlugField(max_length=65, unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=165,)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65,)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/',
                              blank=True,
                              default='',
                              )
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 default=None,
                                 )
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               default=None,
                               )
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe", args=(self.id,))

    @staticmethod
    def resize_image(image, new_width=1280) -> None:
        image_full_path: str = os.path.join(MEDIA_ROOT, image.name)
        print(image_full_path)
        image_pillow = Image.open(image_full_path)
        og_width, og_height = image_pillow.size

        if og_width > new_width:
            new_height = round((new_width * og_height) / og_width)
            new_image = image_pillow.resize(
                (new_width, new_height), Image.LANCZOS
                )
            new_image.save(image_full_path,
                           optimize=True,
                           quality=100,
                           )

    def save(self, *args, **kwargs) -> None:
        range_letter: str = ''.join(
            SystemRandom().choices(
                st.ascii_letters + st.digits,
                k=5
            ),
            )
        self.slug = slugify(f'{self.title}-{range_letter}')

        if self.cover:
            try:
                self.resize_image(self.cover, 800)
            except FileNotFoundError:
                ...

        return super().save(*args, **kwargs)
