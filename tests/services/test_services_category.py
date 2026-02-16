import pytest
from quiz.models import Category
from quiz.services.category import CategoryService


@pytest.mark.django_db
class TestCategoryService:

    def setup_method(self):
        self.service = CategoryService()

    def test_create_category(self):
        category = self.service.create_category("Science")
        assert category.title == "Science"
        assert Category.objects.count() == 1

    def test_get_category(self):
        category = Category.objects.create(title="History")
        fetched = self.service.get_category(category.id)
        assert fetched.id == category.id

    def test_update_category(self):
        category = Category.objects.create(title="Old")
        updated = self.service.update_category(category.id, {"title": "New"})
        assert updated.title == "New"

    def test_delete_category(self):
        category = Category.objects.create(title="Temp")
        self.service.delete_category(category.id)
        assert Category.objects.count() == 0
