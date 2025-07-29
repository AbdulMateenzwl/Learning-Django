from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        user = self.request.user

        if user.is_superuser:
            return []  

        if user.is_staff and self.request.method in ["GET", "POST"]:
            return []

        if not user.is_staff and not user.is_superuser and self.request.method == "GET":
            return []

        from rest_framework.permissions import BasePermission
        class DenyAll(BasePermission):
            def has_permission(self, request, view):
                return False

        return [DenyAll()]
