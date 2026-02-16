"""Модуль с контроллерами для вопросов"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from quiz.services.question import QuestionService
from quiz.serializers import QuestionSerializer

question_service = QuestionService()


class QuestionListCreateView(APIView):
    """GET /api/question, POST /api/question"""

    def get(self, request):
        questions = question_service.list_questions()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = question_service.create_question(
            serializer.validated_data["quiz"].id, serializer.validated_data
        )
        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_201_CREATED
        )


class QuestionDetailView(APIView):
    """GET, PUT, DELETE /api/question/<id>"""

    def get(self, request, pk):
        question = question_service.get_question(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = question_service.update_question(
            pk, serializer.validated_data
        )
        return Response(QuestionSerializer(question).data)

    def delete(self, request, pk):
        question_service.delete_question(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionByTextView(APIView):
    """GET /api/question/by_text/<query>"""

    def get(self, request, query):
        questions = question_service.get_questions_by_text(query)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionCheckAnswerView(APIView):
    """POST /api/question/<id>/check"""

    def post(self, request, pk):
        answer = request.data.get("answer")
        if answer is None:
            return Response(
                {"error": "Answer field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_correct = question_service.check_answer(pk, answer)
        return Response({"correct": is_correct})
