import pytest
from django.urls import reverse

from quiz.models import Quiz


@pytest.mark.django_db
class TestQuizAPI:

    def test_create_quiz(self, client):
        url = reverse("quiz-create")
        response = client.post(
            url,
            {
                "title": "Physics",
                "description": "Physics quiz"
            },
            content_type="application/json",
        )

        assert response.status_code == 201

    def test_get_quiz_by_title(self, client):
        Quiz.objects.create(title="Physics")

        url = reverse("quiz-by-title", kwargs={"title": "Physics"})
        response = client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Physics"
