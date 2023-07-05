from django.urls import include, path
from rest_framework import routers

from api.views import TaskViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
