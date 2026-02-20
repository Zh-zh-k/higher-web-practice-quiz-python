import pytest

from conftest import TEST_CATEGORY_TITLE, UPDATED_CATEGORY_TITLE
from quiz.models import Category


@pytest.mark.django_db
class TestCategoryService:

    def test_create_category(self, category_service):
        before_count = Category.objects.count()
        category = category_service.create_category(TEST_CATEGORY_TITLE)
        after_count = Category.objects.count()
        assert category.title == TEST_CATEGORY_TITLE
        assert after_count == before_count + 1

    def test_get_category(self, category_service, category):
        fetched = category_service.get_category(category.id)
        assert fetched.id == category.id

    def test_update_category(self, category_service, category):
        updated = category_service.update_category(
            category.id,
            {"title": UPDATED_CATEGORY_TITLE},
        )
        assert updated.title == UPDATED_CATEGORY_TITLE

    def test_delete_category(self, category_service, category):
        before_count = Category.objects.count()
        category_service.delete_category(category.id)
        after_count = Category.objects.count()
        assert after_count == before_count - 1
