import pytest

from quiz.models import Category


TEST_CATEGORY_TITLE = "Test Category"
UPDATED_CATEGORY_TITLE = "Updated Category"


@pytest.fixture
def category():
    return Category.objects.create(title=TEST_CATEGORY_TITLE)


@pytest.fixture
def category_service():
    from quiz.services.category import CategoryService
    return CategoryService()
