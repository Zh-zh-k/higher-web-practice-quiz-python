"""Модуль c сериализаторами"""

from rest_framework import serializers
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
            raise serializers.ValidationError("Options must be a list")

        if len(value) < 2:
            raise serializers.ValidationError(
                "There must be at least two answer options"
            )

        return value

    def validate(self, attrs):
        """Проверка, что correct_answer присутствует в options"""

        options = attrs.get("options")
        correct_answer = attrs.get("correct_answer")

        if options and correct_answer and correct_answer not in options:
            raise serializers.ValidationError(
                {"correct_answer": "Correct answer must be one of the options"}
            )

        return attrs
