from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters, status, serializers
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer


class TaskStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['all', 'completed', 'not_completed'], required=False)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="Retrieve, create, update, or delete tasks.",
        responses={200: openapi.Response(description='Success')},
        manual_parameters=[
            openapi.Parameter(
                name='status',
                in_=openapi.IN_QUERY,
                description='Filter tasks by status (all, completed, not_completed).',
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        query_serializer=TaskStatusSerializer
    )
    def list(self, request, *args, **kwargs):
        status = request.query_params.get('status', None)

        if status == 'completed':
            queryset = self.queryset.filter(completed=True)
        elif status == 'not_completed':
            queryset = self.queryset.filter(completed=False)
        else:
            queryset = self.queryset.all()

        self.queryset = queryset

        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new task.",
        responses={201: openapi.Response(description='Task created successfully')}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response({'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update an existing task.",
        responses={200: openapi.Response(description='Task updated successfully')}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response({'message': 'Task updated successfully'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a task.",
        responses={200: openapi.Response(description='Task deleted successfully')}
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_200_OK)
