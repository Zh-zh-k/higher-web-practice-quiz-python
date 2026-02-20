"""Модуль с реализацией сервиса вопросов"""

import random
from django.shortcuts import get_object_or_404

from core.constants import CATEGORY_FIELD
from quiz.dao import AbstractQuestionService
from quiz.models import Question, Quiz, Category
from quiz.utils import update_instance


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов"""

    def list_questions(self) -> list[Question]:
        return list(Question.objects.all())

    def get_question(self, question_id: int) -> Question:
        return get_object_or_404(Question, id=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        return list(Question.objects.filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        return list(Question.objects.filter(quiz_id=quiz_id))

    def create_question(self, quiz_id: int, data: dict) -> Question:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        category = get_object_or_404(Category, id=data.get(CATEGORY_FIELD))

        question = Question.objects.create(
            quiz=quiz,
            category=category,
            text=data.get("text"),
            description=data.get("description"),
            options=data.get("options"),
            correct_answer=data.get("correct_answer"),
            explanation=data.get("explanation"),
            difficulty=data.get("difficulty"),
        )

        return question

    def update_question(self, question_id: int, data: dict) -> Question:
        if CATEGORY_FIELD in data:
            data[CATEGORY_FIELD] = get_object_or_404(
                Category,
                id=data[CATEGORY_FIELD],
            )

        return update_instance(Question, question_id, data)

    def delete_question(self, question_id: int) -> None:
        get_object_or_404(Question, id=question_id).delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        question = get_object_or_404(Question, id=question_id)
        return question.correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        questions = Question.objects.filter(quiz_id=quiz_id)

        if not questions.exists():
            raise Question.DoesNotExist("Вопросы для квиза не найдены")

        return random.choice(list(questions))
