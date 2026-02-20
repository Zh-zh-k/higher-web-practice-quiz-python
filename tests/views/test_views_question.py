import pytest
from django.urls import reverse

from quiz.models import Category, Difficulty, Question, Quiz


@pytest.mark.django_db
class TestQuestionAPI:

    def test_check_answer(self, client):
        quiz = Quiz.objects.create(title="Math")
        category = Category.objects.create(title="Algebra")

        question = Question.objects.create(
            quiz=quiz,
            category=category,
            text="2+2?",
            options=["3", "4"],
            correct_answer="4",
            difficulty=Difficulty.EASY,
        )

        url = reverse("question-check-answer", kwargs={"pk": question.id})
        response = client.post(
            url,
            {"answer": "4"},
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json()["correct"] is True
