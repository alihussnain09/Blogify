from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, UserRegistrationView, CommentViewSet,TagViewSet, CategoryAPIView
from .views_v2 import BlogPostViewSetV2
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


router = DefaultRouter()
router.register(r'blogs',BlogPostViewSet)
router.register(r'comments',CommentViewSet)
router.register(r'tags',TagViewSet)

router_v2 = DefaultRouter()
router_v2.register(r'blogs',BlogPostViewSetV2)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/v2/', include(router_v2.urls)),
    path('categories/', CategoryAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='category-detail'),
    path('api/register',UserRegistrationView.as_view(),name='user-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]