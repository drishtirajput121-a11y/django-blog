from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)
from . import views

# Router auto-generates URL patterns for all ViewSets:
#   GET    /api/blogs/       → BlogViewSet.list
#   POST   /api/blogs/       → BlogViewSet.create
#   GET    /api/blogs/{id}/  → BlogViewSet.retrieve
#   PUT    /api/blogs/{id}/  → BlogViewSet.update
#   PATCH  /api/blogs/{id}/  → BlogViewSet.partial_update
#   DELETE /api/blogs/{id}/  → BlogViewSet.destroy
router = DefaultRouter()
router.register(r'blogs', views.BlogViewSet, basename='blog')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'about', views.AboutViewSet, basename='about')
router.register(r'social-links', views.SocialLinkViewSet, basename='sociallink')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # ── JWT Token Endpoints ──
    # POST /api/token/         → send username+password, get access+refresh tokens
    # POST /api/token/refresh/ → send refresh token, get new access token
    # POST /api/token/verify/  → verify if a token is still valid
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # ── Router-generated CRUD URLs ──
    path('', include(router.urls)),
]
