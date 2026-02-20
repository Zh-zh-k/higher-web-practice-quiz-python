"""Модуль с контроллерами для квизов"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import QuizSerializer
from quiz.services.quiz import QuizService

quiz_service = QuizService()


class QuizListCreateView(APIView):
    """GET /api/quiz, POST /api/quiz"""

    def get(self, request):
        quizzes = quiz_service.list_quizzes()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = quiz_service.create_quiz(serializer.validated_data)
        return Response(
            QuizSerializer(quiz).data,
            status=status.HTTP_201_CREATED
        )


class QuizDetailView(APIView):
    """GET, PUT, DELETE /api/quiz/<id>"""

    def get(self, request, pk):
        quiz = quiz_service.get_quiz(pk)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = quiz_service.update_quiz(pk, serializer.validated_data)
        return Response(QuizSerializer(quiz).data)

    def delete(self, request, pk):
        quiz_service.delete_quiz(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizByTitleView(APIView):
    """GET /api/quiz/by_title/<title>"""

    def get(self, request, title):
        quizzes = quiz_service.get_quizes_by_title(title)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class QuizRandomQuestionView(APIView):
    """GET /api/quiz/<id>/random_question"""

    def get(self, request, pk):
        from quiz.services.question import QuestionService

        question_service = QuestionService()
        question = question_service.random_question_from_quiz(pk)
        from quiz.serializers import QuestionSerializer

        serializer = QuestionSerializer(question)
        return Response(serializer.data)
