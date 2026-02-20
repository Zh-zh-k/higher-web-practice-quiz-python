import pytest

from quiz.models import Category, Difficulty, Question, Quiz
from quiz.services.question import QuestionService


@pytest.mark.django_db
class TestQuestionService:

    def setup_method(self):
        self.service = QuestionService()

    def test_create_question(self):
        quiz = Quiz.objects.create(title="Math")
        category = Category.objects.create(title="Algebra")

        data = {
            "category": category.id,
            "text": "2+2?",
            "description": "",
            "options": ["3", "4"],
            "correct_answer": "4",
            "difficulty": Difficulty.EASY,
        }

        question = self.service.create_question(quiz.id, data)

        assert question.text == "2+2?"
        assert question.quiz == quiz
        assert question.category == category

    def test_check_answer_correct(self):
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

        result = self.service.check_answer(question.id, "4")
        assert result is True
