from django.urls import path, include
from rest_framework.routers import DefaultRouter
from management.views import *



from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Project Management API",
        default_version="v1",
        description="Interactive documentation for the API",
        contact=openapi.Contact(email="workinprogress.bibash@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


# Initialize the router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'projectmembers', ProjectMemberViewSet, basename='projectmember')  # Add this line

urlpatterns = [
    # Authentication-related endpoints
    path('users/register/', CustomUserRegistration.as_view(), name='user-register'),
    path('users/login/', CustomUserLogin.as_view(), name='user-login'),

    # Include the router-generated URLs
    path('', include(router.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]






