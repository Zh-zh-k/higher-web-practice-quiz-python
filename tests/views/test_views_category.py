import pytest
from django.urls import reverse
from quiz.models import Category


@pytest.mark.django_db
class TestCategoryAPI:

    def test_create_category(self, client):
        url = reverse("category-create")
        response = client.post(
            url,
            {"title": "History"},
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_get_category(self, client):
        category = Category.objects.create(title="Science")

        url = reverse("category-detail", kwargs={"pk": category.id})
        response = client.get(url)

        assert response.status_code == 200
        assert response.json()["title"] == "Science"

    def test_delete_category(self, client):
        category = Category.objects.create(title="Temp")

        url = reverse("category-detail", kwargs={"pk": category.id})
        response = client.delete(url)

        assert response.status_code == 204
