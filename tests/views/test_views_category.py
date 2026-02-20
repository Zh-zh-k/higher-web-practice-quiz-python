import pytest
from django.urls import reverse
from rest_framework import status

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
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_category(self, client):
        category = Category.objects.create(title="Science")

        url = reverse("category-detail", kwargs={"pk": category.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Science"

    def test_delete_category(self, client):
        category = Category.objects.create(title="Temp")

        url = reverse("category-detail", kwargs={"pk": category.id})
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
