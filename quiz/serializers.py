"""Модуль c сериализаторами"""

from rest_framework import serializers

from core.constants import MIN_OPTIONS
from quiz.models import Category, Quiz, Question


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        model = Category
        fields = ["id", "title"]


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для квизов"""

    class Meta:
        model = Quiz
        fields = ["id", "title", "description"]


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов"""

    class Meta:
        model = Question
        fields = [
            "id",
            "quiz",
            "category",
            "text",
            "description",
            "options",
            "correct_answer",
            "explanation",
            "difficulty",
        ]

    def validate_options(self, value):
        """Проверка, что options - список минимум из двух элементов"""

        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Варианты ответов должны быть списком"
            )

        if len(value) < MIN_OPTIONS:
            raise serializers.ValidationError(
                "Должно быть минимум два варианта ответа"
            )

        return value

    def validate(self, attrs):
        """Проверка, что correct_answer присутствует в options"""

        options = attrs.get("options")
        correct_answer = attrs.get("correct_answer")

        if options and correct_answer and correct_answer not in options:
            raise serializers.ValidationError(
                {"correct_answer": "Правильный ответ должен быть в вариантах"}
            )

        return attrs
