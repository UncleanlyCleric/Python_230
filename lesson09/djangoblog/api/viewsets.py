from blogging.models import Post, Category
from serializers import PostSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class BloggingViewSet(viewsets.ViewSet):
    '''
    API endpoint that allows users to view blog posts.
    '''

    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
