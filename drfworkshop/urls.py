from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from polls.views import AdminPollViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'polls', AdminPollViewSet, basename='polls')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'api/', include(router.urls)),
]
