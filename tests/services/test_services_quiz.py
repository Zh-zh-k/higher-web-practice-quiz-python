import pytest

from quiz.models import Quiz
from quiz.services.quiz import QuizService


@pytest.mark.django_db
class TestQuizService:

    def setup_method(self):
        self.service = QuizService()

    def test_create_quiz(self):
        data = {
            "title": "Physics",
            "description": "Physics quiz"
        }

        quiz = self.service.create_quiz(data)

        assert quiz.title == "Physics"
        assert quiz.description == "Physics quiz"

    def test_get_quiz(self):
        quiz = Quiz.objects.create(title="Math")

        fetched = self.service.get_quiz(quiz.id)
        assert fetched.id == quiz.id

    def test_get_quiz_by_title(self):
        Quiz.objects.create(title="Biology")

        quizes = self.service.get_quizes_by_title("Biology")

        assert len(quizes) == 1
        assert quizes[0].title == "Biology"

    def test_delete_quiz(self):
        quiz = Quiz.objects.create(title="Temp")
        self.service.delete_quiz(quiz.id)
        assert Quiz.objects.count() == 0
