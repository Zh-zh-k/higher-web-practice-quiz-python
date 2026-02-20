"""Модуль с контроллерами для категорий"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from quiz.services.category import CategoryService
from quiz.serializers import CategorySerializer

category_service = CategoryService()


class CategoryListCreateView(APIView):
    """GET /api/category, POST /api/category."""

    def get(self, request):
        categories = category_service.list_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = category_service.create_category(
            **serializer.validated_data
        )
        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )


class CategoryDetailView(APIView):
    """GET, PUT, DELETE /api/category/<id>."""

    def get(self, request, pk):
        category = category_service.get_category(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = category_service.update_category(
            pk, serializer.validated_data
        )
        return Response(CategorySerializer(category).data)

    def delete(self, request, pk):
        category_service.delete_category(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
