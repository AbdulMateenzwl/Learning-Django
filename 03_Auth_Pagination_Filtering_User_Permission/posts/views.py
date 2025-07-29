from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from .models import Post
from .serializers import PostSerializer
from .permission import RoleBasedPermission

from .pagination import CustomPagination


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [RoleBasedPermission]
    # There are other pagination too, like page based - with fixed page size, limit offset pagination, cursor based pagination
    # but we have customized it
    pagination_class = CustomPagination

    filterset_fields = ["title"]  # Only filter on these fields

    search_fields = ["content"]

    ordering_fields = ["title"]
    ordering = ["title"]

