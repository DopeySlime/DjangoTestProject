from typing import Dict, TypeVar

from django.db.models import Model, QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from .models import Task
from .serializers import TaskSerializer

TModel = TypeVar('TModel', bound=Model)


class CRUDViewSet(viewsets.ModelViewSet):
    create_response: Dict[str, str] = {'message': 'Resource created successfully'}
    update_response: Dict[str, str] = {'message': 'Resource updated successfully'}
    delete_response: Dict[str, str] = {'message': 'Resource deleted successfully'}

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer: ModelSerializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response({_: self.create_response[_] for _ in self.create_response if _ in ['message']},
                        status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args, **kwargs) -> Response:
        partial: bool = kwargs.pop('partial', False)
        instance: TModel = self.get_object()
        serializer: ModelSerializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response({_: self.update_response[_] for _ in self.update_response if _ in ['message']},
                        status=status.HTTP_200_OK)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance: TModel = self.get_object()
        self.perform_destroy(instance)
        return Response({_: self.delete_response[_] for _ in self.delete_response if _ in ['message']},
                        status=status.HTTP_200_OK)


class TaskViewSet(CRUDViewSet):
    queryset: QuerySet = Task.objects.all()
    serializer_class: ModelSerializer = TaskSerializer

    create_response: Dict[str, str] = {
        'message': 'Task created successfully',
        'description': 'Create a new task.'
    }
    update_response: Dict[str, str] = {
        'message': 'Task updated successfully',
        'description': 'Update an existing task.'
    }
    delete_response: Dict[str, str] = {
        'message': 'Task deleted successfully',
        'description': 'Delete a task.'
    }

    @swagger_auto_schema(
        operation_description="Retrieve, create, update, or delete tasks.",
        responses={200: openapi.Response(description='Success')},
        manual_parameters=[
            openapi.Parameter(
                name='status',
                in_=openapi.IN_QUERY,
                description='Filter tasks by status (all, completed, not_completed).',
                type=openapi.TYPE_STRING,
                required=False,
                enum=['all', 'completed', 'not_completed'],
            )
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        compilation_status: str = request.query_params.get('status', None)

        if compilation_status == 'completed':
            queryset: QuerySet[Task] = self.queryset.filter(completed=True)
        elif compilation_status == 'not_completed':
            queryset: QuerySet[Task] = self.queryset.filter(completed=False)
        else:
            queryset: QuerySet[Task] = self.queryset.all()

        self.queryset = queryset

        return super().list(request, *args, **kwargs)


TaskViewSet.create = swagger_auto_schema(
    operation_description=TaskViewSet.create_response['description'],
    responses={201: openapi.Response(description=TaskViewSet.create_response['message'])}
)(TaskViewSet.create)

TaskViewSet.update = swagger_auto_schema(
    operation_description=TaskViewSet.update_response['description'],
    responses={200: openapi.Response(description=TaskViewSet.update_response['message'])}
)(TaskViewSet.update)

TaskViewSet.destroy = swagger_auto_schema(
    operation_description=TaskViewSet.delete_response['description'],
    responses={200: openapi.Response(description=TaskViewSet.delete_response['message'])}
)(TaskViewSet.destroy)
