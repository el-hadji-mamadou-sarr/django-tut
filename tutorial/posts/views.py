from rest_framework import viewsets, status
from .models import PostModel
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """

    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]
        
    @swagger_auto_schema(
            operation_description='post creation',
            responses={201:openapi.Response('Post created', PostSerializer)},
            response_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'exempleTest':openapi.Schema(type=openapi.TYPE_STRING, description='exemple description')
                }
            )
    )
    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            print(request.user)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        post = get_object_or_404(PostModel, pk=post_id)
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        post = get_object_or_404(PostModel, pk=post_id)

        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
       post_id = kwargs.get('pk')
       post = get_object_or_404(PostModel, pk=post_id)
       post.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)

