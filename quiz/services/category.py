"""Модуль с реализацией сервиса категорий"""
from django.shortcuts import get_object_or_404

from quiz.dao import AbstractCategoryService
from quiz.models import Category


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий"""

    def list_categories(self) -> list[Category]:
        return list(Category.objects.all())

    def get_category(self, category_id: int) -> Category:
        return get_object_or_404(Category, id=category_id)

    def create_category(self, title: str) -> Category:
        return Category.objects.create(title=title)

    def update_category(self, category_id: int, data: dict) -> Category:
        category = get_object_or_404(Category, id=category_id)

        for field, value in data.items():
            setattr(category, field, value)

        category.save()
        return category

    def delete_category(self, category_id: int) -> None:
        category = get_object_or_404(Category, id=category_id)
        category.delete()
