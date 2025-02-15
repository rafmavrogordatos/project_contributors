from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SkillViewSet, ProjectViewSet, ApplicationViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'applications', ApplicationViewSet, basename='applications')

urlpatterns = [
    path('', include(router.urls)),  
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

