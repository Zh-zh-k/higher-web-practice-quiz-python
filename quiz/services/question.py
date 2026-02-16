"""Модуль с реализацией сервиса вопросов"""

import random
from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuestionService
from quiz.models import Question, Quiz, Category


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
        category = get_object_or_404(Category, id=data.get("category"))

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
        question = get_object_or_404(Question, id=question_id)

        for field, value in data.items():
            if field == "category":
                category = get_object_or_404(Category, id=value)
                setattr(question, "category", category)
            else:
                setattr(question, field, value)

        question.save()
        return question

    def delete_question(self, question_id: int) -> None:
        question = get_object_or_404(Question, id=question_id)
        question.delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        question = get_object_or_404(Question, id=question_id)
        return question.correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        questions = Question.objects.filter(quiz_id=quiz_id)

        if not questions.exists():
            raise Question.DoesNotExist("No questions found for this quiz.")

        return random.choice(list(questions))
