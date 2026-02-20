"""Модуль c моделями приложения quiz"""

from django.db import models
from django.core.exceptions import ValidationError

from core.constants import (
    DIFFICULTY_MAX_LENGTH,
    MIN_OPTIONS,
    TITLE_MAX_LENGTH,
    TEXT_MAX_LENGTH,
    REPR_MAX_LENGTH
)


class Category(models.Model):
    """Модель категории вопросов"""

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        unique=True,
        null=False,
        verbose_name='Название'
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.title


class Quiz(models.Model):
    """Модель квиза"""

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        null=False,
        verbose_name='Название'
    )

    description = models.CharField(
        max_length=TEXT_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Квиз"
        verbose_name_plural = "Квизы"

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
        related_name='questions',
        verbose_name='Квиз'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Категория'
    )

    text = models.CharField(
        max_length=TEXT_MAX_LENGTH,
        null=False,
        verbose_name='Текст вопроса'
    )

    description = models.CharField(
        max_length=TEXT_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    options = models.JSONField(
        null=False,
        help_text='Список вариантов ответа (минимум два)',
        verbose_name='Варианты ответов'
    )

    correct_answer = models.CharField(
        max_length=TEXT_MAX_LENGTH,
        null=False,
        verbose_name='Правильный ответ'
    )

    explanation = models.CharField(
        max_length=TEXT_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Объяснение'
    )

    difficulty = models.CharField(
        max_length=DIFFICULTY_MAX_LENGTH,
        choices=Difficulty.choices,
        null=False,
        verbose_name='Сложность'
    )

    class Meta:
        ordering = ["quiz"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        return f'Вопрос #{self.id}: {self.text[:REPR_MAX_LENGTH]}'

    def clean(self) -> None:
        """Валидация бизнес-логики вопроса"""

        if not isinstance(self.options, list):
            raise ValidationError('Варианты ответа должны быть списком')

        if len(self.options) < MIN_OPTIONS:
            raise ValidationError('Должно быть минимум два варианта ответа')

        if self.correct_answer not in self.options:
            raise ValidationError(
                'Правильный ответ должен быть вреди вариантов ответа'
            )
