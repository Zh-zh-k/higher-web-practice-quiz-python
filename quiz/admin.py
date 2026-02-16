from django.contrib import admin
from .models import Category, Quiz, Question


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)
    ordering = ("id",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("title",)
    ordering = ("id",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "quiz",
        "difficulty",
        "created_at",
    )
    list_filter = ("difficulty", "quiz", "quiz__category")
    search_fields = ("text",)
    ordering = ("id",)
