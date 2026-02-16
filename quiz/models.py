"""Модуль c моделями приложения quiz"""

from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Модель категории вопросов"""

    title = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.title


class Quiz(models.Model):
    """Модель квиза"""

    title = models.CharField(
        max_length=200,
        blank=False,
        null=False,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self) -> str:
        return self.title


class Difficulty(models.TextChoices):
    """Варианты сложностей для вопросов"""

    EASY = 'easy', 'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'


class Question(models.Model):
    """Модель вопроса"""

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    text = models.CharField(
        max_length=500,
        blank=False,
        null=False,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    options = models.JSONField(
        blank=False,
        null=False,
        help_text="Список вариантов ответа (минимум два)",
    )

    correct_answer = models.CharField(
        max_length=500,
        blank=False,
        null=False,
    )

    explanation = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    difficulty = models.CharField(
        max_length=6,
        choices=Difficulty.choices,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def clean(self) -> None:
        """Валидация бизнес-логики вопроса"""

        if not isinstance(self.options, list):
            raise ValidationError("Options must be a list.")

        if len(self.options) < 2:
            raise ValidationError("There must be at least two answer options.")

        if self.correct_answer not in self.options:
            raise ValidationError("Correct answer must be one of the options.")

    def __str__(self) -> str:
        return f"Question #{self.id}: {self.text[:50]}"
