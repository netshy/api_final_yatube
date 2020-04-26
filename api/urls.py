from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

router = DefaultRouter()

router.register(r'^api/v1/posts', PostViewSet)
router.register(r'^api/v1/posts/(?P<post_id>\d+)/comments', CommentViewSet, basename="comment")
router.register(r'^api/v1/group', GroupViewSet, basename="group")
router.register(r'^api/v1/follow', FollowViewSet, basename="follow")

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
