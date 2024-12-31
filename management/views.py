from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import User, Project, Task, Comment, ProjectMember
from .serializers import *


# Custom User Registration View
class CustomUserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


# Custom User Login View
class CustomUserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key,
            "message": "Login successful."
        }, status=status.HTTP_200_OK)


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Project ViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('members__user', 'tasks').all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Return only projects the user owns or is a member of
        return self.queryset.filter(
            members__user=self.request.user
        ).distinct()


# ProjectMember ViewSet
class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.select_related('project', 'user').all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return self.queryset.filter(project__id=project_id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()


# Task ViewSet
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('project', 'assigned_to').all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return self.queryset.filter(project__id=project_id)
        return self.queryset

    def perform_create(self, serializer):
        assigned_to = serializer.validated_data.get('assigned_to', None)
        serializer.save(assigned_to=assigned_to or self.request.user)


# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user', 'task').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.request.query_params.get('task_id')
        if task_id:
            return self.queryset.filter(task__id=task_id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
